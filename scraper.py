import constants
import csv


def generate_field_params(initial_id: int) -> str:
    params = list()
    params.append(constants.armySerialNumber)
    for i in range(initial_id, initial_id + 9):
        params.append(',')
        params.append(i)

    return ''.join(params)


def get_state_ids() -> None:
    with open(constants.state_id_file_name) as state_id_file:
        data = csv.reader(state_id_file)
        for row in data:
            constants.state_ids.append(row[0])
