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

STATE_IDS = list()

FIELDED_SEARCH_URL: str = 'https://aad.archives.gov/aad/fielded-search.jsp?dt=893'
STATE_PARAMS: str = """cl_24996=41%2CD1%2CM1%2C02%2CR0%2CN9%2CO5%2CK8%2CO7%2CJ9%2C98%2CI8%2CR8%2C87%2CH7%2CQ7%2CK7%2C00%2CK6%2CL0%2CK5%2CL8%2CL7%2CK4%2CK9%2CN6%2C91%2CI1%2CR1%2CJ8%2CQ1%2C70%2CG0%2CP0%2C11%2CA1%2CJ1%2C!6%2CX6%2CX8%2C!8%2C21%2CB1%2CK1%2C34%2CC4%2CL4%2CJ0%2CM0%2CQ2%2C42%2CD2%2CM2%2C09%2CL5%2CL6%2C43%2CD3%2CM3%2CN7%2C!2%2CX2%2C!9%2CX9%2C03%2CL9%2C!3%2CX3%2C92%2CI2%2CR2%2CO4%2C61%2CF1%2CO1%2C51%2CE1%2CN1%2C72%2CG2%2CP2%2CP1%2CO0%2CQ0%2CN8%2C73%2CG3%2CP3%2C52%2CE2%2CN2%2CO8%2CM9%2C88%2CH8%2CQ8%2CO6%2C12%2CA2%2CJ2%2C31%2CC1%2CL1%2C13%2CA3%2CJ3%2CX1%2C!1%2C62%2CF2%2CO2%2C74%2CG4%2CP4%2C45%2CD5%2CM5%2C75%2CG5%2CP5%2C93%2CI3%2CR3%2C76%2CG6%2CP6%2C94%2CI4%2CR4%2C14%2CA4%2CJ4%2C22%2CB2%2CK2%2C83%2CH3%2CQ3%2C23%2CB3%2CK3%2CX5%2C!5%2C46%2CD6%2CM6%2C77%2CG7%2CP7%2CM4%2C53%2CE3%2CN3%2C84%2CH4%2CQ4%2C95%2CI5%2CR5%2CX7%2C!7%2C06%2CJ7%2C32%2CC2%2CL2%2C07%2CN0%2C08%2C15%2CA5%2CJ5%2CN5%2CO9%2CX4%2C!4%2C47%2CD7%2CM7%2C78%2CG8%2CP8%2C48%2CD8%2CM8%2C85%2CH5%2CQ5%2C01%2CK0%2C96%2CI6%2CR6%2C16%2CA6%2CJ6%2C33%2CC3%2CL3%2C97%2CI7%2CR7%2C54%2CE4%2CN4%2C63%2CF3%2CO3%2C79%2CG9%2CP9"""
STATE_ID_FILE_NAME = '../resources/cl_2046.csv'

PAGE_NEXT_CSS_SELECTOR = '#results-section > form > div:nth-child(7) > a:nth-child(13)'
# results-section > form > div:nth-child(7) > a:nth-child(11)
# results-section > form > div:nth-child(7) > a:nth-child(11)
PAGE_NEXT_XPATH = '//*[@id="results-section"]/form/div[2]/a[10]'

SEARCH_BUTTON_CSS_SELECTOR = '#content > p:nth-child(6) > input:nth-child(2)'
