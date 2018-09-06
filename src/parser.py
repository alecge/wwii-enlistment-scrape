from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

from record import Record


class Parser:
    def __init__(self, path: str):
        self.__records: List[Record] = list()
        self.__hTreeml: BeautifulSoup = None

        self.doc_fp = Path(path).open()
        self.__hTreeml = BeautifulSoup(self.doc_fp)

    def __process_records(self) -> List[Record]:
        table = self.__hTreeml['queryResults']

        thead: Tag = table.thead
        tbody: Tag = table.tbody

        for tr in tbody.children:
            





        return None

    def get_records(self) -> List[Record]:
        if not self.__records:
            self.__process_records()

        return self.__records
