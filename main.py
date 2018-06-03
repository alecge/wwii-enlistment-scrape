from scraper import *
import constants

# Assume army serial number is always the same
# First go over army serial number in one pass
# Then go over subsequent fields always including the army serial number so a cross reference can be made

# Populates the state_ids list from constants.py
populate_state_ids()

prev_field_id: int = constants.STARTING_ID

while True:
    param_str, prev_field_id = generate_field_params(prev_field_id)

    get_data_from_fields(constants.FIELDED_SEARCH_URL + param_str)