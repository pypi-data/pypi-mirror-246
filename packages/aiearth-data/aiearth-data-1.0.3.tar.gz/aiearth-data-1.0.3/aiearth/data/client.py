import os
from typing import Optional

from aiearth.core.client import Endpoints
from aiearth.core.client.client import BaseClient
from aiearth.core.env import set_log_level
from pystac import Item

from aiearth import core
from aiearth.data.search import *
from aiearth.data.stac_id import StacId

set_log_level('info')

AIE_AUTH_TOKEN = "x-aie-auth-token"


def __get_host__() -> str:
    host = Endpoints.HOST
    data_host = os.getenv("DATA_CLIENT_HOST")
    return data_host if (data_host is not None and len(data_host) > 0) else host


def __get_token__() -> str:
    return core.g_var.get_var(core.g_var.GVarKey.Authenticate.TOKEN) or None


def __get_client__(from_type: FromType) -> Client:
    root = f"{__get_host__()}/{from_type.value}/stac"
    if from_type.value == FromType.PERSONAL.value:
        root += "/personal/raster"
    return Client.open(root, headers={
        AIE_AUTH_TOKEN: __get_token__()
    })


def __get_stac_content__(stac_id: StacId) -> Optional[Item]:
    if FromType.PERSONAL.value == stac_id.get_from_type().value:
        catalog = personaldata_client()
        result = list(catalog.search(ids=stac_id.get_stac_id()).items())
        if not result or len(result) == 0:
            return None
        return result[0]
    elif FromType.OPEN.value == stac_id.get_from_type().value:
        catalog = opendata_client()
        result = list(catalog.search(ids=stac_id.get_stac_id()).items())
        if not result or len(result) == 0:
            return None
        return result[0]


def __get_bytes__(stac_id: StacId,
                  x_offset: int,
                  y_offset: int,
                  x_size: int,
                  y_size: int,
                  band_name: str) -> (bytearray, str, int):
    if x_size * y_size > 10000 * 10000:
        raise ValueError("暂不支持获取该尺寸的数据")

    from_type = stac_id.get_from_type().value
    stac_id_str = stac_id.get_stac_id()
    request_id = core.client.endpoints.newUUID()
    url = f"{Endpoints.HOST}/tesla/api/data/raster/{from_type}/{stac_id_str}/action/read?" \
          f"xOffset={x_offset}&yOffset={y_offset}&xSize={x_size}&ySize={y_size}&bandName={band_name}"
    resp = BaseClient.get(url, hdrs={"x-aie-request-id": request_id, "Accept-Encoding": "gzip"})
    if resp.status_code != 200:
        raise ValueError(f"服务异常，请联系平台服务, 请求ID {request_id}")
    return resp.content, resp.headers.get("x-aie-datatype"), int(resp.headers.get("x-aie-datasize"))
