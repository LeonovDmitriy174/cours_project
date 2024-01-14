from utils import (open_json, sorted_function,
                   executed_operations, required_quantity,
                   config_date, Operation)

quantity = input(f'Какое количество последних операция вы хотите увидеть?\n')

while quantity.isalpha():
    quantity = input(f'Введите пожалуйста целое число\n')


operations_list = required_quantity(config_date(executed_operations(sorted_function(open_json('operations.json')))),
                                    int(quantity))

for operation in operations_list:
    print(Operation(operation).masked_from())
