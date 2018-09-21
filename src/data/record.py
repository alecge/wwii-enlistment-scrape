import copy
import logging
from typing import Dict
from typing import List


class Record:
    def __init__(self):
        self.__data: Dict[str, str] = dict()
        self.__log = logging.getLogger('record.Record')

        pass

    def add_field(self, field_name: str, field_value: str) -> None:
        if not field_name:
            self.__log.error("Field name is null...THAT CANNOT BE")
            raise TypeError("Invalid None type given as field name")

        self.__data[field_name] = field_value

    def get_field_names(self) -> List[str]:
        return list(self.__data.keys())

    def get_fields(self) -> Dict[str, str]:
        return self.__data
