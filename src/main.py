from scraper import *
import logging
from pathlib import Path
from time import sleep

import constants


# Assume army serial number is always the same
# First go over army serial number in one pass
# Then go over subsequent fields always including the army serial number so a cross reference can be made


def main():
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

    try:
        scraper.init_driver()
        scraper.scrape()
    except Exception as err_msg:
        log.error('Crash on page #' + str(scraper.get_previous_page()))
        log.error('Something went wrong: ', exc_info=True)
        raise
    finally:
        scraper.quit()

    # # Populates the state_ids list from constants.py
    # populate_state_ids()
    #
    # prev_field_id: int = constants.STARTING_ID
    #
    # while True:
    #     param_str, prev_field_id = generate_field_params(prev_field_id)
    #
    #     try:
    #         get_data_from_fields(constants.FIELDED_SEARCH_URL + '&' + param_str)
    #     except TimeoutException:
    #         continue
    #
    #     if prev_field_id > constants.ENDING_ID:
    #         browser.close()
    #         break
    #
    # print('ALL DONE!!!!')


main()
