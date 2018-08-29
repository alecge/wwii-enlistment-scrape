from scraper import *
import logging

from selenium.common.exceptions import TimeoutException

import constants

# Assume army serial number is always the same
# First go over army serial number in one pass
# Then go over subsequent fields always including the army serial number so a cross reference can be made


def main():

    logging.basicConfig(level=logging.DEBUG)
    log = logging.getLogger(__name__)

    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    try:
        scraper = Scraper()
        scraper.scrape()
    except Exception as err_msg:
        log.error('Something went wrong: ', exc_info=True)
        raise

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
