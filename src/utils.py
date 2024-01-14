import json
import os
from datetime import datetime


def open_json(filename):
    with open(os.path.join(filename), encoding='utf-8') as file:
        operations_list = json.loads(file.read())
    return operations_list


def sorted_function(operations_list):
    for index, operation in enumerate(operations_list):
        try:
            operation['date'] == 0
        except KeyError:
            del operations_list[index]
    sorted_list = sorted(operations_list, key=lambda x: (x['date']), reverse=True)
    return sorted_list


def executed_operations(sorted_operations_list):
    operations_list = []
    for operation in sorted_operations_list:
        if operation['state'] == 'EXECUTED':
            operations_list.append(operation)
    return operations_list


def config_date(operations):
    for index, operation in enumerate(operations):
        the_datetime = datetime.fromisoformat(operation['date'])
        the_date = the_datetime.date()
        operations[index]['date'] = f'{the_date.day}.{the_date.month}.{the_date.year}'
    return operations


def required_quantity(operations, quantity):
    return operations[:quantity]


class Operation:
    def __init__(self, operation):
        self.date = operation['date']
        self.description = operation['description']
        self.to = f'Счет **{operation['to'][-4:]}'
        self.amount = operation['operationAmount']['amount']
        self.name = operation['operationAmount']['currency']['name']
        try:
            operation['from'][0] == 'С'
        except KeyError:
            self.from_ = 'Информация отсутствует'
        else:
            self.from_ = operation['from']

    def __repr__(self):
        return (f'{self.date} {self.description}\n'
                f'{self.from_} -> {self.to}\n'
                f'{self.amount} {self.name}\n')

    def masked_from(self):
        number = 0
        if self.from_[0] == 'С':
            self.from_ = f'Счет **{self.from_[-4:]}'
        else:
            for i, value in enumerate(self.from_):
                if not value.isdigit():
                    continue
                else:
                    number += 1
                    if number == 4 or number == 9 or number == 14:
                        self.from_ = self.from_[: i + 1] + ' ' + self.from_[i + 1:]
                    if 7 < number < 10 or 10 < number < 15:
                        self.from_ = self.from_[: i] + '*' + self.from_[i + 1:]
        return (f'{self.date} {self.description}\n'
                f'{self.from_} -> {self.to}\n'
                f'{self.amount} {self.name}\n')
