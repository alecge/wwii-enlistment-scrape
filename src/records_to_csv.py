import csv
import logging
from pathlib import Path
from typing import List

from record import Record


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

        self.__records: List[Record] = list()

    def add_to_csv(self, *args: Record) -> None:
        if None in args:
            # TODO: raise exception
            raise ValueError("Cannot add None to CSV!!")

        self.__records.extend(args)

    def write(self) -> None:
        if not self.__records:
            # TODO: log
            raise ValueError("Cannot write zero records to csv!")

        with self.__path.open(mode='w', newline='') as csvfile:
            field_names = self.__records[0].get_field_names()
            writer = csv.DictWriter(csvfile, fieldnames=field_names)

            writer.writeheader()
            for record in self.__records:
                writer.writerow(record.get_fields())
