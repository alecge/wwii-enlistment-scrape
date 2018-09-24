import logging
from pathlib import Path
from typing import Set, List

from conversion.html_parser import Parser
from conversion.records_to_csv import RecordsToCsv
from data.record import Record
from database.database import setup_db, Database

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def write_to_db(db_config: str):
    db = setup_db(db_config)

#
# # TODO: replace absolute paths with path passed in from argparse
# def convert_to_csv():
#     converter = RecordsToCsv('/home/alec/scraped-data/')
#
#     folder_path: Path = Path('/home/alec/scraped-data').resolve(strict=True)
#
#     first_run = True
#     files_read: Set[str] = set()
#
#     for subfolder in folder_path.iterdir():
#         log.info('Working through ' + str(subfolder))
#         if subfolder.is_dir():
#             for file in subfolder.iterdir():
#
#                 if file.parts[-1] not in files_read:
#                     records = Parser(str(file)).parse()
#                     files_read.add(file.parts[-1])
#                     if first_run:
#                         first_run = False
#                         converter.init_csv(records[0].get_field_names())
#
#                     log.debug('Parsing file ' + file.parts[-1])
#                     converter.add_to_csv(*records)
#
#     converter.done()


def convert(data_dir: str, db_config: str):
    fpath: Path = Path(data_dir).resolve(strict=True)
    converter = RecordsToCsv(data_dir)

    files_read: Set[str] = set()
    first_run = True

    db = setup_db(db_config)

    for subfolder in fpath.iterdir():
        log.info('Working through ' + str(subfolder))

        if subfolder.is_dir():
            for file in subfolder.iterdir():

                if file.parts[-1] not in files_read:
                    records = Parser(str(file)).parse()

                    if first_run:
                        first_run = False
                        converter.init_csv(records[0].get_field_names())

                    write_out(converter, db, records)

        elif 'html' in subfolder.parts:
            records = Parser(str(subfolder)).parse()
            write_out(converter, db, records)


def write_out(converter: RecordsToCsv, db: Database, records: List[Record]) -> None:
    converter.add_to_csv(*records)
    db.add(*records)


convert('/home/alec/scraped-data',
        '/home/alec/Documents/Projects/wwii-enlistment-scrape/postgres_info')
