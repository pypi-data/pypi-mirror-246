from abc import ABC
from enum import Enum


class FromType(Enum):
    """
    数据类型
    """
    PERSONAL = "personal"
    OPEN = "open"


class StacId(ABC):
    """
    数据唯一ID
    """

    def __init__(self, stac_id: str, from_type: FromType):
        """
        数据ID表达
        :param stac_id: 数据唯一ID
        :param from_type: 数据类型
        """
        self.__stac_id = stac_id
        self.__from_type = from_type

    def get_stac_id(self) -> str:
        """
        获取数据ID
        :return: 数据ID
        """
        return self.__stac_id

    def get_from_type(self) -> FromType:
        """
        获取数据类型
        :return: 数据类型
        """
        return self.__from_type


class PersonalStacId(StacId):
    """
    个人数据唯一ID表达
    """
    def __init__(self, stac_id: str):
        super(PersonalStacId, self).__init__(stac_id, FromType.PERSONAL)


class OpenStacId(StacId):
    """
    公开数据唯一ID表达
    """
    def __init__(self, stac_id: str):
        super(OpenStacId, self).__init__(stac_id, FromType.OPEN)

