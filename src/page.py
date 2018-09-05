from typing import List

from record import Record


class Page:
    def __init__(self):
        self.__records: List[Record] = list()

        pass

    def add_record(self, record: Record) -> None:
        pass

    def get_records(self) -> List[Record]:
        pass

