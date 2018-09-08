from typing import Dict
import logging


class Record:
    def __init__(self):
        self.__data: Dict[str, str] = Dict[str, str]()
        self.__log = logging.getLogger('record.Record')

        pass

    def add_field(self, field_name: str, field_value: str) -> None:
        if not field_name:
            self.__log.error("Field name is null...THAT CANNOT BE")
            raise TypeError("Invalid None type given as field name")

        self.__data[field_name] = field_value
