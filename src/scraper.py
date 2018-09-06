import csv
import datetime
import logging
import os
from pathlib import Path
from typing import List
from typing import Set
from typing import Tuple
import re

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver

from selenium.common.exceptions import NoSuchElementException

import constants

# TODO
# Do the following things
# - Add resume mechanism so that it can resume from the page it left off.  I need to change
#   the folder naming convention to something that will be consistent across runs of the same page
# - Add prevention mechanism: It will quit the chrome driver every ~500 pages or so to work around
#   the issue with "[1536196465.016][SEVERE]: Timed out receiving message from renderer: -0.013"
# - Maybe try adding a docker healthcheck for the chrome container so that we might be able to rely
#   on Docker to fix this issue.  If I do this I also have to add a recovery mechanism where if
#   it times out I can try quickly a couple of times, then retry after delays (time the time it
#   takes the chrome container to come up and then make sure it tries like every 5 seconds,
#   potentially infinitely
# - Maybe pass through the docker socket so that I can control the docker spawning from inside the
#   python container.  This seems pretty complicated but here's a link to start:
#   https://stackoverflow.com/questions/38362415/how-can-i-connect-to-a-server-using-python-sockets-inside-a-docker-container


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
                                                  desired_capabilities=DesiredCapabilities.CHROME,
                                                  options='--disable-gpu')
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

        # self.__browser.implicitly_wait(3)

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

    def __get_page_info(self) -> Tuple[int, int]:
        page_text: str = str()
        try:
            page_text = self.__browser.find_element_by_css_selector('#content > '
                                                                    'div:nth-child(''3)').text
        except NoSuchElementException as not_found:
            self.log.exception('Couldn\'t identify page number!', exc_info=True)
            raise

        match = re.match('Page (\d+) of (\d+)', page_text)
        if match:
            return int(match.group(1)), int(match.group(2))
        else:
            self.log.exception('Page number invalid!', exc_info=True)
            raise ValueError('Could not match regex to the data on page')

    def __get_current_page(self) -> int:
        current_page, total_pages = self.__get_page_info()
        self.log.debug('Current page: ' + str(current_page))
        return current_page

    def __get_num_pages(self) -> int:
        current_page, total_pages = self.__get_page_info()
        self.log.debug('Total pages: ' + str(total_pages))
        return total_pages

    def __init_instance_folders(self, volume_folder_path: Path, bind_folder_path: Path) -> Tuple[
        Path, Path]:
        volume_data = (volume_folder_path / datetime.datetime.now().strftime(
            '%Y-%m-%d-%H:%M:%S')).resolve()
        if not volume_data.exists():
            self.log.debug('Creating folder ' + str(volume_data))
            volume_data.mkdir()

        bind_data = (bind_folder_path / datetime.datetime.now().strftime(
            '%Y-%m-%d-%H:%M:%S')).resolve()
        if not bind_data.exists():
            self.log.debug('Creating folder ' + str(bind_data))
            bind_data.mkdir()

        self.log.debug('Created folders for this search\'s data')

        return volume_data, bind_data

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
            for option in self.__browser.find_element_by_id('rpp').find_elements_by_tag_name(
                    'option'):
                if option.text == '50':
                    option.click()
                    break

            # Save the current URL without the &pg=n argument for reuse over and over
            url: str = self.__browser.current_url
            if start_page > 1:
                # It is GUARANTEED that the first page we download is the start page
                self.__browser.get(url + '&pg=' + str(start_page))

            # Folders for this particular run
            volume_data, bind_data = self.__init_instance_folders(volume_folder_path,
                                                                  bind_folder_path)

            self.log.info('Downloading HTML')

            while True:

                cur_page = self.__get_current_page()

                # Used for file naming by page.
                # Each file name is the page number padded to 6 digits with zeros
                volume_file_name = str(cur_page).zfill(6) + '.html'
                volume_file_path = volume_data / volume_file_name

                bind_file_name = str(cur_page).zfill(6) + '.html'
                bind_file_path = bind_data / bind_file_name

                with volume_file_path.open(mode='w') as volume_outfile, bind_file_path.open(
                        mode='w') as bind_outfile:
                    volume_outfile.write(self.__browser.page_source)
                    self.log.debug("Wrote to file at " + str(volume_file_path))

                    bind_outfile.write(self.__browser.page_source)
                    self.log.debug("Wrote to file at " + str(bind_file_path))

                if cur_page < self.__get_num_pages():
                    self.__browser.get(url + '&pg=' + str(cur_page + 1))
                else:
                    self.log.info('Finished...onto the next one')
                    break

                self.previous_page = cur_page

            self.log.info('Finished this batch of requests!')

            self.__browser.close()

            if has_reached_end:
                self.log.info("All finished..yay!")
                return
