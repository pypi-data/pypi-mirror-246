import math
import struct
from typing import Optional, List
from typing import Union

import numpy as np
from aiearth.core import g_var
from pyproj import CRS, Transformer
from pystac import Item
from shapely import box, Polygon

from aiearth.data import client
from aiearth.data.stac_id import StacId

import logging

logger = logging.getLogger(__name__)

log_lvl = 'INFO'
if g_var.has_var(g_var.GVarKey.Log.LOG_LEVEL):
    log_lvl = g_var.get_var(g_var.GVarKey.Log.LOG_LEVEL).upper()

logging.basicConfig(level=log_lvl)

BASE_CLIP_NUM = 256


class DataLoaderConfig(object):
    buffer_clip_size = 1024 * 1024


def transform(item: Item, bbox: Union[List[int], tuple], from_crs: Union[CRS, int], asset_key: str):
    """
    将地理坐标，或者投影坐标，通过使用pyproj转换为影像的行列坐标
    :param item: 影像 stac Item, 包含了影像的投影六参数
    :param bbox: 任意的bbox，同时标注from_crs; bbox只接受 (minx, miny, maxx, maxy) 格式；也即左下，右上坐标
    :param from_crs: bbox的CRS信息，可以为 pyproj.CRS, 可以为EPSG code, 如 4326
    :param asset_key: 目标波段的asset，因为波段分辨率不一致的原因，此处需要指定波段名称
    :return: 转换bbox得到的行列坐标
    """

    # transform bbox to target crs bbox
    transformer: Transformer = Transformer.from_crs(from_crs, item.properties['proj:epsg'], always_xy=True)
    transformed_bbox = transformer.transform_bounds(left=bbox[0], bottom=bbox[1], right=bbox[2], top=bbox[3])
    # calculate item bbox in target crs

    if item.properties.get("proj:transform") is not None:
        stac_transform = item.properties.get("proj:transform")
    else:
        stac_transform = item.assets[asset_key].extra_fields['proj:transform']
    upper_left_x = stac_transform[2]
    pixel_width = stac_transform[0]
    upper_left_y = stac_transform[5]
    pixel_height = stac_transform[4]
    if item.assets.get(asset_key) is not None and item.assets.get(asset_key).extra_fields.get("proj:shape") is not None:
        width, height = item.assets[asset_key].extra_fields['proj:shape']
    else:
        width, height = item.properties.get("proj:shape")
    bottom_right_x = upper_left_x + width * abs(pixel_width)
    bottom_right_y = upper_left_y - height * abs(pixel_height)
    item_bbox = (upper_left_x, bottom_right_y, bottom_right_x, upper_left_y)
    # check transformed-bbox and item's bbox has intersection, return intersection bbox if intersected
    transformed_bbox_polygon: Polygon = box(*transformed_bbox)
    item_bbox_polygon: Polygon = box(*item_bbox)
    intersected = transformed_bbox_polygon.intersects(item_bbox_polygon)
    if not intersected:
        raise ValueError(f"输入bbox {bbox} 转换后 {transformed_bbox} 与 item 的 bbox {item_bbox} 没有交集")
    else:
        transformed_bbox_polygon = transformed_bbox_polygon.intersection(item_bbox_polygon)
    transformed_bbox = transformed_bbox_polygon.bounds
    # use item's geoTransform and transformed-bbox to get the row-column index(offset) and size
    x_offset = abs(transformed_bbox[0] - item_bbox[0]) / abs(pixel_width)
    y_offset = abs(transformed_bbox[3] - item_bbox[3]) / abs(pixel_height)
    x_size = abs(transformed_bbox[2] - transformed_bbox[0]) / abs(pixel_width)
    y_size = abs(transformed_bbox[3] - transformed_bbox[1]) / abs(pixel_height)
    return math.floor(x_offset), math.floor(y_offset), math.ceil(x_size), math.ceil(y_size)


def __adjust_size__(size):
    if size < 0:
        raise ValueError(size)
    if size < BASE_CLIP_NUM:
        return BASE_CLIP_NUM

    i = 1
    while True:
        choice = BASE_CLIP_NUM * i
        next_choice = choice + BASE_CLIP_NUM
        if choice <= size < next_choice:
            return choice
        i += 1


class DataLoader(object):
    """
    数据装载器，根据数据的唯一ID(STAC_ID)来识别数据，执行数据的分片获取
    """

    def __init__(self, stac_id: StacId):
        """
        数据装载器的初始化，使用数据唯一ID
        :param stac_id:
        """
        self.__stac__ = None
        self.__stac_id = stac_id

    def load(self):
        """
        执行装载识别
        :return: 无返回
        """
        self.__stac__ = client.__get_stac_content__(self.__stac_id)

    def get_stac(self) -> Optional[Item]:
        """
        获取数据的STAC信息
        :return:
        """
        return self.__stac__

    def block(self,
              band_name: str,
              offset_size: Union[List[int], tuple] = None,
              bbox: Union[List[float], tuple] = None,
              bbox_crs: Union[int, CRS] = CRS(4326),
              ) -> np.ndarray:
        """
        通过影像的行列索引或者bbox信息获取影像的切片
        :param band_name: 目标波段
        :param offset_size: list or tuple of (x_offset, y_offset, x_size, y_size) offset和bbox必须二选一, 同时出现优先使用offset_size
        :param bbox: (min_x, min_y, max_x, max_y) or (west, south, east, north) 和offset必须二选一
        :param bbox_crs: 指定bbox的坐标系参数，如果不指定，默认为 EPSG:4326
        :return: ndarray of (rows, columns) or (y_size, x_size)
        """
        if offset_size is not None:
            x_offset, y_offset, x_size, y_size = offset_size
        else:
            x_offset, y_offset, x_size, y_size = transform(self.__stac__, bbox, bbox_crs, band_name)
            logger.info(f"Transformed {bbox} to x_offset: {x_offset}, "
                        f"y_offset: {y_offset}, x_size: {x_size}, y_size: {y_size}")

        if x_size * y_size <= DataLoaderConfig.buffer_clip_size:
            return self.__clip__(x_offset, y_offset, x_size, y_size, band_name)
        else:
            # using sliding window to get all
            # 使用sliding window的办法进行逐个切片获取
            sqrt_buffer_width = sqrt_buffer_height = int(math.sqrt(DataLoaderConfig.buffer_clip_size))
            buffer_width = buffer_height = __adjust_size__(sqrt_buffer_width)
            logger.info(
                f"切片像素个数 {x_size * y_size} 超过了既定 DataLoaderConfig.clip_size {DataLoaderConfig.buffer_clip_size}"
                f"\n\t 取math.sqrt({DataLoaderConfig.buffer_clip_size}) 为 {sqrt_buffer_height}"
                f"\n\t 调整滑动窗口大小为{BASE_CLIP_NUM}倍数 {buffer_height}")
            # 计算列切片的个数
            width_grid = int(x_size / buffer_width) + (0 if x_size % buffer_width == 0 else 1)
            # 计算行切片的个数
            height_grid = int(y_size / buffer_height) + (0 if y_size % buffer_height == 0 else 1)

            channel = np.ndarray(shape=(y_size, x_size))
            for h in range(height_grid):
                for w in range(width_grid):
                    this_x_offset = buffer_width * w
                    this_y_offset = buffer_height * h
                    this_buffer_width = buffer_width if this_x_offset + buffer_width <= x_size else x_size - this_x_offset
                    this_buffer_height = buffer_height if this_y_offset + buffer_height <= y_size else y_size - this_y_offset
                    block = self.__clip__(x_offset + this_x_offset, y_offset + this_y_offset, this_buffer_width,
                                          this_buffer_height, band_name)
                    channel[this_y_offset: this_y_offset + this_buffer_height,
                    this_x_offset: this_x_offset + this_buffer_width] = block
            return channel

    def __clip__(self, x_offset, y_offset, x_size, y_size, band_name):
        block_bytes, data_type, data_bit_size = client.__get_bytes__(self.__stac_id,
                                                                     x_offset=x_offset,
                                                                     y_offset=y_offset,
                                                                     x_size=x_size,
                                                                     y_size=y_size,
                                                                     band_name=band_name)
        _format = None
        if "DT_UInt16" == data_type:
            _format = "H"
        elif "DT_Int16" == data_type:
            _format = "h"
        elif "DT_Byte" == data_type:
            _format = "B"
        elif "DT_UInt32" == data_type:
            _format = "I"
        elif "DT_Int32" == data_type:
            _format = 'i'
        elif "DT_Float32" == data_type:
            _format = "f"
        elif "DT_Float64" == data_type:
            _format = "d"
        else:
            raise ValueError(f"Unknown data type {data_type}")

        final_array = list(struct.iter_unpack(_format, block_bytes))
        return np.array(final_array).reshape([y_size, x_size])
