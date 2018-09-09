from records_to_csv import RecordsToCsv
from parser import Parser
from pathlib import Path
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def convert_to_csv():
    converter = RecordsToCsv('/home/alec/scraped-data/')

    folder_path: Path = Path('/home/alec/scraped-data').resolve(strict=True)

    first_run = True

    for subfolder in folder_path.iterdir():
        log.debug('Working through ' + str(subfolder))
        if subfolder.is_dir():
            for file in subfolder.iterdir():
                records = Parser(str(file)).parse()

                if first_run:
                    first_run = False
                    converter.init_csv(records[0].get_field_names())
                    print(records[0].get_field_names())

                converter.add_to_csv(*records)

    converter.done()


convert_to_csv()
