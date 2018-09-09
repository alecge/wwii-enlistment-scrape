import copy
import logging
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup
from bs4.element import Tag

from record import Record


class Parser:
    def __init__(self, path: str):
        self.__records: List[Record] = list()
        self.log = logging.getLogger('parser.Parser')
        self.__hTreeml = None

        try:
            with Path(path).open('r') as doc:
                self.__hTreeml = BeautifulSoup(doc.read(), 'html.parser')
        except FileNotFoundError:
            self.log.exception("File doesn't exist!", exc_info=True)
            raise

    def __process_records(self) -> None:
        """

        :return:
        """

        if self.__hTreeml is None:
            self.log.exception("Does the HTML file exist? Parser couldn't initialize itself")
            raise ValueError("HTML failed to load, cannot continue")

        table: Tag = self.__hTreeml.find(id="queryResults")
        if not table:
            self.log.error("Could not find results section in HTML!")
            # TODO: raise exception?
            return

        field_name_row = table.thead.tr
        field_names: list = list()
        for th in field_name_row.children:
            if th != "\n" and "View Record" not in th.string:
                field_names.append(th.string)

        for tr in table.tbody.children:
            if not isinstance(tr, str):
                self.log.debug('TR element is ' + str(tr))
                temp_rec: Record = Record()

                # There are extraneous '\n' and other strings so get rid of them
                # First tag in the list is an <img> element with a link so we discard it
                no_strings: List[Tag] = [x for x in tr.contents if not isinstance(x, str)][1:]

                print(no_strings)

                for field_name, td in zip(field_names, no_strings):
                    temp_rec.add_field(field_name, td.string)

                self.__records.append(temp_rec)

    def parse(self) -> List[Record]:
        if not self.__records:
            self.__process_records()

        return copy.deepcopy(self.__records)
