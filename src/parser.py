from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

from record import Record
import logging


class Parser:
    def __init__(self, path: str):
        self.__records: List[Record] = list()
        self.log = logging.getLogger('parser.Parser')

        try:
            self.doc_fp = Path(path).open('r')
        except FileNotFoundError:
            self.log.exception("File doesn't exist!", exc_info=True)
            raise

        self.__hTreeml = BeautifulSoup(self.doc_fp, 'html.parser')

    def __process_records(self) -> List[Record]:
        """

        :return:
        """

        table: Tag = self.__hTreeml.find(id="queryResults")
        if not table:
            self.log.error("Could not find results section in HTML!")
            return None

        field_name_row = table.thead.tr
        field_names: list = list()
        for th in field_name_row.children:
            if th != "\n" and "View Record" not in th.string:
                field_names.append(th.string)

        table_body: Tag = table.tbody
        for tr in table_body.children:
            temp_rec = Record()
            for td, field_name in zip(tr.contents[1:], field_names):
                temp_rec.add_field(field_name, td.string)

            self.__records.append(temp_rec)

        return None

    def get_records(self) -> List[Record]:
        if not self.__records:
            self.__process_records()

        return self.__records
