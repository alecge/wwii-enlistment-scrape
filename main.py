from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from scraper import *

import constants

# Set the driver to the prebuilt docker container running on the same machine
browser = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                           desired_capabilities=DesiredCapabilities.CHROME)

# Assume army serial number is always the same
# First go over army serial number in one pass
# Then go over subsequent fields always including the army serial number so a cross reference can be made

# Populates the state_ids list from constants.py
get_state_ids()

prev_field_id: int = constants.armySerialNumber

while prev_field_id <= constants.ending_id:
    current_url: str = generate_field_params(prev_field_id)
    prev_field_id += 9
    browser.get(current_url)






