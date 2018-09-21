import csv
import logging
from pathlib import Path
from typing import List

from data.record import Record


class RecordsToCsv:
    """
    RecordsToCsv maintains one assumption: That all records have the same exact fields,
    not one more or one less.

    Breaking that invariant will cause problems!!!
    """

    def __init__(self, folder_path: str, file_name='enlistments.csv'):
        self.__log: logging.Logger = logging.getLogger('record_to_csv.RecordToCsv')

        try:
            self.__path: Path = Path(folder_path).resolve(strict=True)
        except FileNotFoundError as not_found:
            self.__path.mkdir(parents=True)
        except RuntimeError as infinite_loop:
            # TODO
            raise

        self.__path = self.__path / file_name
        self.__csvfile = self.__path.open(mode='w', newline='')
        self.__csvwriter: csv.DictWriter = None

    def init_csv(self, field_names: List[str]):
        if not field_names:
            raise ValueError("Cannot write none as headers to csv")

        self.__csvwriter = csv.DictWriter(self.__csvfile, fieldnames=field_names)
        self.__csvwriter.writeheader()

    def add_to_csv(self, *args: Record) -> None:
        if None in args or args is None:
            # TODO: raise exception
            raise ValueError("Cannot add None to CSV!!")

        for record in args:
            self.__csvwriter.writerow(record.get_fields())

    def done(self) -> None:
        self.__csvfile.close()