import constants
import csv

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


# Set the driver to the prebuilt docker container running on the same machine
print("browser bois?")
browser = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',
                           desired_capabilities=DesiredCapabilities.CHROME)
print("huh")


def generate_field_params(initial_id: int) -> str:
    params = list(str)

    for i in range (initial_id, initial_id + 7):
        if i not in constants.CONSTANT_FIELDS:
            list.append('sc=')
            list.append(i)
            list.append('&')
    
    return ''.join(params)


def get_state_ids() -> None:
    with open(constants.STATE_ID_FILE_NAME) as state_id_file:
        data = csv.reader(state_id_file)
        for row in data:
            constants.state_ids.append(row[0])


def get_data_from_fields(url: str) -> None:
    # Get the fielded search url
    browser.get(url=url)

    # Click the search button
    browser.find_element_by_link_text('Search').click()
    browser.implicitly_wait(2)
    i = 0

    for option in browser.find_element_by_id('rpp').find_elements_by_tag_name('option'):
        if option.text == '50':
            option.click()
            break

    while True:
        # TODO: save the page source to a file
        with open('/root/' + str(i) + '.html', 'w') as outfile:
            outfile.write(browser.page_source)

        if not browser.find_element_by_link_text('Next >'):
            break
        else:
            # Hit next page
            browser.find_element_by_link_text('Next >').click()
            browser.implicitly_wait(2)

        i += 1

    pass
