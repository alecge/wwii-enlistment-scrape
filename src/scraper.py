import constants
import csv

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement

from pathlib import Path

import os

from typing import List
from typing import Tuple

# Set the driver to the prebuilt docker container running on the same machine
browser = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                           desired_capabilities=DesiredCapabilities.CHROME)


def generate_field_params(initial_id: int) -> Tuple[str, int]:
    params: List[str] = list()

    # Append the field IDs that will always be needed
    for field in constants.CONSTANT_FIELDS:
        params.append('sc=')
        params.append(str(field))
        params.append('&')

    cur_id = initial_id
    num_params = 0

    # Do while loop
    # If
    while True:
        params.append('sc=')

        # If the current field ID (cur_id) is not already added and it is smaller than the largest possible ID,
        # Add the current field ID to the params list
        if cur_id not in params and cur_id <= constants.ENDING_ID:
            params.append(str(cur_id))
            num_params += 1

        cur_id += 1

        # If we are at the maximum number of parameters and
        if num_params >= 7:
            break
        else:
            params.append('&')

    return ''.join(params), int(params[-1])


def populate_state_ids() -> None:
    with open(constants.STATE_ID_FILE_NAME) as state_id_file:
        data = csv.reader(state_id_file)
        for row in data:
            constants.STATE_IDS.append(row[0])

    # Pop the first item off because the csv file's first row is "Code"
    constants.STATE_IDS = constants.STATE_IDS[1:]


def get_data_from_fields(url: str) -> None:

    print('===================')
    print('Searching URL {}'.format(url))

    # Get the fielded search url
    browser.get(url=url)

    select_all_states()

    # Click the search button
    for potentialSearchButton in browser.find_elements_by_tag_name('input'):
        if 'Search' in potentialSearchButton.get_attribute('outerHTML'):
            potentialSearchButton.click()
            break

    for option in browser.find_element_by_id('rpp').find_elements_by_tag_name('option'):
        if option.text == '50':
            option.click()
            break

    folder_path = str(Path.home()) + '/' + url.replace('/', '')
    if not os.path.exists(folder_path):
        print('Creating folder {}'.format(folder_path))
        os.mkdir(folder_path)

    print('Downloading all pages...', end='', flush=True)
    i = 1
    while True:
        file_path = folder_path + '/' + str(i).zfill(5) + '.html'

        with open(file_path, 'w') as outfile:
            outfile.write(browser.page_source)

        if not browser.find_element_by_link_text('Next >'):
            break
        else:
            # Hit next page
            browser.find_element_by_link_text('Next >').click()
            browser.implicitly_wait(2)

        i += 1

    print('Done')
    print('===================')
    browser.close()


def select_all_states() -> None:
    print('Selecting all states...', end='', flush=True)

    main_window = browser.current_window_handle

    state_row: WebElement = browser.find_element_by_link_text('RESIDENCE: STATE').parent
    state_row.find_element_by_link_text('Select from Code List').click()

    popup_window = browser.window_handles[1]
    browser.switch_to.window(popup_window)

    browser.implicitly_wait(3)

    test = list()

    for inputBox in browser.find_elements_by_tag_name('input'):
        if 'Submit' in inputBox.get_attribute('outerHTML'):
            test.append(inputBox)
        elif 'window.close()' not in inputBox.get_attribute('outerHTML'):
            inputBox.click()

    print('Done')

    # Click the submit button
    test[0].click()

    browser.switch_to.window(main_window)
