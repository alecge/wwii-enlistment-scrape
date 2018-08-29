import csv
import datetime
import logging
import os
from pathlib import Path
from typing import List
from typing import Set
from typing import Tuple

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement

import constants


#
# browser = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
#                            desired_capabilities=DesiredCapabilities.CHROME)

#
# def generate_field_params(initial_id: int) -> Tuple[str, int]:
#     params: List[str] = list()
#
#     # Append the field IDs that will always be needed
#     for field in constants.CONSTANT_FIELDS:
#         params.append('sc=')
#         params.append(str(field))
#         params.append('&')
#
#     cur_id = initial_id
#     num_params = 0
#
#     # Do while loop
#     # If
#     while True:
#         params.append('sc=')
#
#         # If the current field ID (cur_id) is not already added and it is smaller than the largest possible ID,
#         # Add the current field ID to the params list
#         if cur_id not in params and cur_id <= constants.ENDING_ID:
#             params.append(str(cur_id))
#             num_params += 1
#
#         cur_id += 1
#
#         # If we are at the maximum number of parameters and
#         if num_params >= 7:
#             break
#         else:
#             params.append('&')
#
#     return ''.join(params), int(params[-1])
#
#
# def populate_state_ids() -> None:
#     with open(constants.STATE_ID_FILE_NAME) as state_id_file:
#         data = csv.reader(state_id_file)
#         for row in data:
#             constants.STATE_IDS.append(row[0])
#
#     # Pop the first item off because the csv file's first row is "Code"
#     constants.STATE_IDS = constants.STATE_IDS[1:]
#
#
# def get_data_from_fields(url: str) -> None:
#     print('===================')
#     print('Searching URL {}'.format(url))
#
#     # Get the fielded search url
#     browser.get(url=url)
#
#     select_all_states()
#
#     # Click the search button
#     for potentialSearchButton in browser.find_elements_by_tag_name('input'):
#         if 'Search' in potentialSearchButton.get_attribute('outerHTML'):
#             potentialSearchButton.click()
#             break
#
#     for option in browser.find_element_by_id('rpp').find_elements_by_tag_name('option'):
#         if option.text == '50':
#             option.click()
#             break
#
#     folder_path = str(Path.home()) + '/' + url.replace('/', '')
#     if not os.path.exists(folder_path):
#         print('Creating folder {}'.format(folder_path))
#         os.mkdir(folder_path)
#
#     print('Downloading all pages...', end='', flush=True)
#     i = 1
#     while True:
#         file_path = folder_path + '/' + str(i).zfill(5) + '.html'
#
#         with open(file_path, 'w') as outfile:
#             outfile.write(browser.page_source)
#
#         if not browser.find_element_by_link_text('Next >'):
#             break
#         else:
#             # Hit next page
#             browser.find_element_by_link_text('Next >').click()
#             browser.implicitly_wait(2)
#
#         i += 1
#
#     print('Done')
#     print('===================')
#     browser.close()
#
#
# def select_all_states() -> None:
#     print('Selecting all states...', end='', flush=True)
#
#     main_window = browser.current_window_handle
#
#     state_row: WebElement = browser.find_element_by_link_text('RESIDENCE: STATE').parent
#     state_row.find_element_by_link_text('Select from Code List').click()
#
#     popup_window = browser.window_handles[1]
#     browser.switch_to.window(popup_window)
#
#     browser.implicitly_wait(3)
#
#     test = list()
#
#     for inputBox in browser.find_elements_by_tag_name('input'):
#         if 'Submit' in inputBox.get_attribute('outerHTML'):
#             test.append(inputBox)
#         elif 'window.close()' not in inputBox.get_attribute('outerHTML'):
#             inputBox.click()
#
#     print('Done')
#
#     # Click the submit button
#     test[0].click()
#
#     browser.switch_to.window(main_window)
#

class Scraper:
    # Set the driver to the prebuilt docker container running on the same machine
    __browser = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                                 desired_capabilities=DesiredCapabilities.CHROME)

    def __init__(self):
        self.scraped_param_ids: Set[int] = set()
        self.log = logging.getLogger(__name__)

    def __generate_params(self) -> Tuple[str, bool]:
        # The list of strings to be folded into a single string representing the
        # parameters string in the url
        request_param_list: List[str] = list()

        # Append the field IDs that will always be needed
        for field in constants.CONSTANT_FIELDS:
            request_param_list.append('&')
            request_param_list.append('sc=')
            request_param_list.append(str(field))

            self.scraped_param_ids.add(field)

        num_fields: int = len(request_param_list) / 3

        for id in constants.FIELD_IDS:
            if num_fields <= 10:

                if id not in self.scraped_param_ids:
                    request_param_list.append('&')
                    request_param_list.append('sc=')
                    request_param_list.append(str(id))

                    num_fields += 1

            else:
                break

        return ''.join(request_param_list), constants.FIELD_IDS[-1] in self.scraped_param_ids

    def __select_all_states(self) -> None:
        self.log.debug('Selecting all states')

        main_window = self.__browser.current_window_handle

        state_row: WebElement = self.__browser.find_element_by_link_text('RESIDENCE: STATE').parent
        state_row.find_element_by_link_text('Select from Code List').click()

        popup_window = self.__browser.window_handles[1]
        self.__browser.switch_to.window(popup_window)

        self.__browser.implicitly_wait(3)

        input_boxes = list()

        # Click all <input> tags that aren't the submit button first because that's
        # bad and closes the window and nono to that
        for inputBox in self.__browser.find_elements_by_tag_name('input'):
            if 'Submit' in inputBox.get_attribute('outerHTML'):
                input_boxes.append(inputBox)
            elif 'window.close()' not in inputBox.get_attribute('outerHTML'):
                inputBox.click()

        self.log.debug('Done selecting states')

        # Click the submit button
        input_boxes[0].click()

        self.__browser.switch_to.window(main_window)

    def scrape(self) -> None:
        self.log.info('Starting scrape')

        data_folder_path = Path.cwd() / '..' / 'data'
        data_folder_path.resolve()
        if not data_folder_path.exists():
            data_folder_path.mkdir()

        while True:
            params, has_reached_end = self.__generate_params()
            self.log.debug('Scraping ' + params)

            self.__browser.get(constants.FIELDED_SEARCH_URL + params)
            self.__select_all_states()

            # Click the search button
            for potentialSearchButton in self.__browser.find_elements_by_tag_name('input'):
                if 'Search' in potentialSearchButton.get_attribute('outerHTML'):
                    potentialSearchButton.click()
                    self.log.debug('Clicked the search button!~~~')
                    break

            # Set to 50 results per page
            for option in self.__browser.find_element_by_id('rpp').find_elements_by_tag_name('option'):
                if option.text == '50':
                    option.click()
                    break

            cur_path = data_folder_path / datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')
            if not cur_path.exists():
                self.log.debug('Creating folder ' + str(cur_path))
                cur_path.mkdir()

            # Used for file naming by page.
            # Each file name is the page number padded to 5 digits with zeros
            counter = 1

            while True:
                file_name = str(counter).zfill(5) + '.html'
                file_path = cur_path / file_name

                with file_path.open(mode='w') as outfile:
                    outfile.write(self.__browser.page_source)
                    self.log.debug("Wrote to file at" + str(file_path))

                    if not self.__browser.find_element_by_link_text('Next >'):
                        self.log.info('Finished...onto the next one')
                        break
                    else:

                        # hit next page
                        self.__browser.find_element_by_link_text('Next >').click()
                        self.__browser.implicitly_wait(2)

                counter += 1

            self.__browser.close()

            if has_reached_end:
                self.log.info("All finished..yay!")
                return
