import logging
from time import sleep

from scraper import *


def run_scraper():
    # Just in case the selenium server isn't up and running yet
    sleep(3)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)

    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    # handler = logging.StreamHandler()
    # handler.setLevel(logging.DEBUG)
    #
    # formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # handler.setFormatter(formatter)
    # log.addHandler(handler)

    scraper = Scraper()
    page_num = 69476

    while True:
        try:
            scraper.init_driver()
            scraper.scrape(page_num)
        except Exception as err_msg:
            log.error('Crash on page #' + str(scraper.get_previous_page()))
            log.error('Something went wrong: ', exc_info=True)
            try:
                scraper.quit()
            except Exception:
                log.exception('Failed to quit scraper')
                pass
            page_num = scraper.get_previous_page()
            continue

        log.info('Retrying...')


def convert_html():
    pass


def main():
    pass


main()
