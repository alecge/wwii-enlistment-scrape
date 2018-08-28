from scraper import *

from selenium.common.exceptions import TimeoutException

import constants

# Assume army serial number is always the same
# First go over army serial number in one pass
# Then go over subsequent fields always including the army serial number so a cross reference can be made


def main():

    scraper = Scraper()
    scraper.scrape()

    # Populates the state_ids list from constants.py
    populate_state_ids()

    prev_field_id: int = constants.STARTING_ID

    while True:
        param_str, prev_field_id = generate_field_params(prev_field_id)

        try:
            get_data_from_fields(constants.FIELDED_SEARCH_URL + '&' + param_str)
        except TimeoutException:
            continue

        if prev_field_id > constants.ENDING_ID:
            browser.close()
            break

    print('ALL DONE!!!!')

main()
