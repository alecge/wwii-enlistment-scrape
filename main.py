from scraper import *
import constants

# Assume army serial number is always the same
# First go over army serial number in one pass
# Then go over subsequent fields always including the army serial number so a cross reference can be made

# Populates the state_ids list from constants.py
# get_state_ids()
#
# prev_field_id: int = constants.ARMY_SERIAL_NUMBER
#
# while prev_field_id <= constants.ENDING_ID:
#     current_url: str = generate_field_params(prev_field_id)
#     prev_field_id += 9
#     browser.get(current_url)

get_data_from_fields('https://aad.archives.gov/aad/fielded-search.jsp?dt=893&tf=&bc=&sc=24994&sc=24995&sc=24996&sc=24998&sc=24997&sc=24993&sc=24981&sc=24983')
