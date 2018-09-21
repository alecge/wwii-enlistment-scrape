from conversion.records_to_csv import RecordsToCsv
from conversion.parser import Parser
from pathlib import Path
import logging
from typing import Set

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def convert_to_csv():
    converter = RecordsToCsv('/home/alec/scraped-data/')

    folder_path: Path = Path('/home/alec/scraped-data').resolve(strict=True)

    first_run = True
    files_read: Set[str] = set()

    for subfolder in folder_path.iterdir():
        log.info('Working through ' + str(subfolder))
        if subfolder.is_dir():
            for file in subfolder.iterdir():

                if file.parts[-1] not in files_read:
                    records = Parser(str(file)).parse()
                    files_read.add(file.parts[-1])
                    if first_run:
                        first_run = False
                        converter.init_csv(records[0].get_field_names())

                    log.debug('Parsing file ' + file.parts[-1])
                    converter.add_to_csv(*records)

    converter.done()
