import os

from config import ROOT_DIR
from src.utils import (open_json, sorted_function,
                       executed_operations, required_quantity,
                       config_date, Operation)


def test_open_json():
    TEST_DATA_PATH = os.path.join(ROOT_DIR, 'tests', 'test_json.json')
    assert open_json(TEST_DATA_PATH) == [
        {'id': 441945886, 'state': 'EXECUTED'}]


test_case_one = [
    {'date': "2018-08-19T04:27:37.904916",
     'state': "CANCELED"},
    {'state': "EXECUTED"},
    {'date': "2019-07-03T18:35:29.512364",
     'state': "CANCELED"}]


def test_sorted_function():
    assert sorted_function(test_case_one) == [
        {'date': "2019-07-03T18:35:29.512364",
         'state': "CANCELED"},
        {'date': "2018-08-19T04:27:37.904916",
         'state': "CANCELED"}
    ]


test_case_two = test_case_one.copy()


def test_executed_operation():
    assert executed_operations(test_case_two) == [{'state': "EXECUTED"}]


test_case_three = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_required_quantity():
    assert required_quantity(test_case_three, 3) == [0, 1, 2]
    assert required_quantity(test_case_three, 6) == [0, 1, 2, 3, 4, 5]


test_case_four = [
    {"date": "2019-08-26T10:50:58.294041"},
    {"date": "2018-03-23T10:45:06.972075"}]


def test_config_date():
    assert config_date(test_case_four) == [
        {'date': '26.8.2019'},
        {'date': '23.3.2018'}]


test_case_five = {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "26.8.2019",
    "operationAmount": {
        "amount": "31957.58",
        "currency": {
            "name": "руб.",
            "code": "RUB"
        }
    },
    "description": "Перевод организации",
    "from": "Maestro 1596837868705199",
    "to": "Счет 64686473678894779589"}
test_case_six = {
    "id": 441945886,
    "state": "EXECUTED",
    "date": "26.8.2019",
    "operationAmount": {
        "amount": "31957.58",
        "currency": {
            "name": "руб.",
            "code": "RUB"
        }
    },
    "description": "Перевод организации",
    "to": "Счет 64686473678894779589"}
test_case_seven = {
    "id": 649467725,
    "state": "EXECUTED",
    "date": "2018-04-14T19:35:28.978265",
    "operationAmount": {
      "amount": "96995.73",
      "currency": {
        "name": "руб.",
        "code": "RUB"
      }
    },
    "description": "Перевод организации",
    "from": "Счет 27248529432547658655",
    "to": "Счет 97584898735659638967"
  }


def test_operation_init():
    assert Operation(test_case_five).date == '26.8.2019'
    assert Operation(test_case_five).masked_from() == ('26.8.2019 Перевод организации\n'
                                                       'Maestro 1596 83** **** 5199 -> Счет **9589\n'
                                                       '31957.58 руб.\n')
    assert Operation(test_case_six).from_ == 'Информация отсутствует'
    assert Operation(test_case_seven).masked_from() == ('2018-04-14T19:35:28.978265 Перевод организации\n'
                                                        'Счет **8655 -> Счет **8967\n'
                                                        '96995.73 руб.\n')
    assert repr(Operation(test_case_five)) == ('26.8.2019 Перевод организации\n'
                                               'Maestro 1596837868705199 -> Счет **9589\n'
                                               '31957.58 руб.\n')
