from aiearth.data.stac_id import FromType
from datetime import datetime
from datetime import timezone

from aiearth.data import client
from pystac_client import Client


def opendata_client() -> Client:
    """
    获取公开数据的STAC client
    :return: STAC_CLIENT
    """
    return client.__get_client__(FromType.OPEN)


def personaldata_client() -> Client:
    """
    获取个人数据的STAC CLIENT
    :return:
    """
    return client.__get_client__(FromType.PERSONAL)


class PersonalQueryBuilder(object):
    """
    个人数据查询Builder
    """

    def __init__(self):
        self.__query__ = {}

    def and_name_contains(self, name_contains: str):
        """
        定义名称的pattern
        :param name_contains: 名称包含
        :return: self
        """
        self.__query__['properties.title'] = {
            "contains": name_contains
        }
        return self

    def and_upload_datetime_between(self, start: datetime, end: datetime):
        """
        定义影像的上传时间范围
        :param start: 上传时间的开始
        :param end: 上传时间的结束
        :return: self
        """
        self.__query__['properties.meta:uploadDatetime'] = {
            "gte": PersonalQueryBuilder.__format(start),
            "lte": PersonalQueryBuilder.__format(end)
        }
        return self

    def build(self) -> dict:
        """
        组装query内容
        :return: STAC client query接口的 query param
        """
        return self.__query__

    @staticmethod
    def __format(dt: datetime) -> str:
        dt = dt.astimezone(timezone.utc)
        dt = dt.replace(tzinfo=None)
        return f'{dt.isoformat("T")}Z'
