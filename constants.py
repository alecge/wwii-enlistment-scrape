INITIAL_FIELD_ID: int = 24979
NUM_FIELDS: int = 25

ARMY_SERIAL_NUMBER: int = 24994

STARTING_ID: int = 24979
ENDING_ID: int = 25004

CONSTANT_FIELDS = [
    ARMY_SERIAL_NUMBER,
    24995,  # name
    24996]  # residence: state

FIELD_IDS = [
    24979,
    24980,
    24981,
    24982,
    24983,
    24984,
    24985,
    24986,
    24987,
    24988,
    24989,
    24990,
    24991,
    24992,
    24993,
    24994,
    24995,
    24996,
    24997,
    24998,
    24999,
    25000,
    25001,
    25002,
    25003,
    25004
]

FIELD_TO_ID: dict = {
    24979: 'term of enlistment',
    24980: 'longevity',
    24981: 'source of army personnel',
    24982: 'nativity',
    24983: 'year of birth',
    24984: 'race and citizenship',
    24985: 'education',
    24986: 'civilian occupation',
    24987: 'box number',
    24988: 'film reel number',
    24989: 'field use as desired',
    24990: 'date of enlistment day',
    24991: 'branch: alpha designation',
    24992: 'date of enlistment month',
    24993: 'date of enlistment year',
    24994: 'army serial number',
    24995: 'name',
    24996: 'residence: state',
    24997: 'place of enlistment',
    24998: 'residence: county',
    24999: 'grade: code',
    25000: 'branch: code',
    25001: 'marital status',
    25002: 'component of the army',
    25003: 'card number',
    25004: 'grade: alpha designation',
}

state_ids = list()

FIELDED_SEARCH_URL: str = 'https://aad.archives.gov/aad/fielded-search.jsp?dt=893'
STATE_ID_FILE_NAME = 'resources/cl_2046.csv'

PAGE_NEXT_CSS_SELECTOR = '#results-section > form > div:nth-child(7) > a:nth-child(13)'
# results-section > form > div:nth-child(7) > a:nth-child(11)
# results-section > form > div:nth-child(7) > a:nth-child(11)
PAGE_NEXT_XPATH = '//*[@id="results-section"]/form/div[2]/a[10]'

SEARCH_BUTTON_CSS_SELECTOR = '#content > p:nth-child(6) > input:nth-child(2)'
