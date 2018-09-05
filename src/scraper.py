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
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.common.exceptions import NoSuchElementException

import constants


class Scraper:

    def __init__(self):
        self.scraped_param_ids: Set[int] = set()
        self.log = logging.getLogger(__name__)
        self.previous_page = 1

        # Set the driver to None so it can be initialized later when needed
        self.__browser: WebDriver = None

    def init_driver(self) -> None:
        if not self.__browser:
            try:
                self.__browser = webdriver.Remote(command_executor='http://chrome:4444/wd/hub',
                                                  desired_capabilities=DesiredCapabilities.CHROME)
            except Exception:
                self.log.exception('Failed to initialize driver!')
                raise

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

    def get_previous_page(self) -> int:
        return self.previous_page

    def quit(self) -> None:
        self.__browser.quit()

    def scrape(self, start_page: int = 1) -> None:

        if not self.__browser:
            self.init_driver()
            self.log.info('Driver not initialized before scraping! Initializing driver...')

        self.log.info('Starting scrape')

        volume_folder_path = Path('/html').resolve()
        bind_folder_path = Path('/scraped-data').resolve()

        if not volume_folder_path.exists() or not bind_folder_path.exists():
            self.log.exception("Folders /html or /scraped-data do not exist!")
            raise FileNotFoundError("Folders /html or /scraped-data do not exist!")

        while True:
            params, has_reached_end = self.__generate_params()  # FIXME: Can use factory pattern instead
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

            volume_data = (volume_folder_path / datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')).resolve()
            if not volume_data.exists():
                self.log.debug('Creating folder ' + str(volume_data))
                volume_data.mkdir()

            bind_data = (bind_folder_path / datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')).resolve()
            if not bind_data.exists():
                self.log.debug('Creating folder ' + str(bind_data))
                bind_data.mkdir()

            # Used for file naming by page.
            # Each file name is the page number padded to 6 digits with zeros
            counter = 1
            self.previous_page = counter

            self.log.info('Downloading HTML')

            while True:

                if counter >= start_page:
                    volume_file_name = str(counter).zfill(6) + '.html'
                    volume_file_path = volume_data / volume_file_name

                    bind_file_name = str(counter).zfill(6) + '.html'
                    bind_file_path = bind_data / bind_file_name

                    with volume_file_path.open(mode='w') as volume_outfile, bind_file_path.open(
                            mode='w') as bind_outfile:
                        volume_outfile.write(self.__browser.page_source)
                        self.log.debug("Wrote to file at " + str(volume_file_path))

                        bind_outfile.write(self.__browser.page_source)
                        self.log.debug("Wrote to file at " + str(bind_file_path))

                if not self.__browser.find_elements_by_link_text('Next >'):
                    self.log.info('Finished...onto the next one')
                    break
                else:
                    for attempt in range(10):
                        try:
                            # hit next page
                            self.__browser.find_element_by_partial_link_text('Next >').click()
                        except Exception as err_msg:
                            self.__browser.refresh()
                            self.__browser.get(self.__browser.current_url)
                            self.log.exception(
                                'Something bad happened when trying to download HTML! Retrying.... Exec info: ',
                                exc_info=True)
                        else:
                            self.log.debug('No problems!')
                            break

                counter += 1

            self.log.info('Finished this batch of requests!')

            self.__browser.close()

            if has_reached_end:
                self.log.info("All finished..yay!")
                return
