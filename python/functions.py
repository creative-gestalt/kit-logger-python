import os
import sys
from . import number_generator, logger
from itertools import tee, islice, chain
from pathlib import Path


green = 'color 2'
red = 'color 4'
light_aqua = 'color B'
member_file = Path('./user_member_numbers/%s/ALL/extras/member_numbers.txt')
group_file = Path('./user_member_numbers/%s/ALL/extras/group_number.txt')


def create_dict(file):
    d = {}
    with open(file) as f:
        for line in f:
            (key, val) = line.split()
            d[str(key)] = val
    return d


def get_keys_by_value(_dict, value):
    keys = list()
    items = _dict.items()
    for item in items:
        if item[1].replace('_', ' ') == value:
            keys.append(str(item[0]))
    return keys


def create_dict_and_filter(file):
    d = {}
    unique = []
    with open(file) as f:
        for line in f:
            (key, val) = line.split()
            d[str(key)] = val
            if val.replace('_', ' ') not in unique:
                unique.append(val.replace('_', ' '))
    return unique


def read_from_file(file):
    with open(file, 'r') as f:
        number = f.read()
    return number


def read_and_append(file):
    some_list = []
    with open(file) as f:
        for line in f:
            some_list.append(line.rstrip())
    return some_list


def write_to_file(file, value):
    with open(file, 'w') as f:
        f.write(value)


def write_lines_to_file(file, value_list):
    with open(file, 'w') as f:
        for item in value_list:
            f.write('%s\n' % item)


def write_list_of_lists(file, value_list):
    with open(file, 'w') as f:
        for item in value_list:
            f.write('%s\n' % item.strip())


def get_kit_amount_and_iteration(kit_count):
    # kits = input('How many kits do you want to log (only enter increments of 10):  ')
    kits = kit_count
    values = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100,
              110, 120, 130, 140, 150, 160, 170, 180, 190, 200,
              210, 220, 230, 240, 250, 260, 270, 280, 290, 300]
    while int(kits) not in values:
        kits = input('You either entered an incorrect value, or it was larger than 100, try again: ')
        if int(kits) in values:
            break
    iterations = int(kits) / 10
    return iterations


def get_group_number(driver):
    if group_file.is_file():
        group_number = read_from_file(group_file)
        return group_number
    else:
        group_number = int(input('Please enter your group number: '))
        if not group_number:
            driver.close()
            logger.message('Group number appears to be empty')
            sys.exit('Values cannot be empty')
        write_to_file(group_file, str(group_number))
        return group_number


def get_member_numbers():
    member_numbers = []
    if member_file.is_file():
        if not os.stat(member_file).st_size == 0:
            some_list = read_and_append(member_file)
            for item in some_list:
                member_numbers.append(item)
            return member_numbers
        else:
            message = 'You have used all Member Numbers in your box'
            print(message)
            logger.message(message)
            some_list = number_generator.generate_card_numbers()
            for item in some_list:
                member_numbers.append(item)
            return member_numbers
    else:
        message = 'Member Numbers don\'t exist yet'
        print(message)
        logger.message(message)
        some_list = number_generator.generate_card_numbers()
        for item in some_list:
            member_numbers.append(item)
        return member_numbers


def find_and_update(old_list, new_list):
    for item in new_list:
        if item in old_list:
            old_list.remove(item)
    return old_list


def update_list_file(file, updated_list):
    with open(file, 'w') as f:
        for item in updated_list:
            f.write('%s\n' % item)


def xpath_string_escape(input_str):
    parts = input_str.split("'")
    return "concat('" + "', \"'\" , '".join(parts) + "', '')"


def previous_and_next(some_iterable):
    prev, items, nex = tee(some_iterable, 3)
    prev = chain([None], prev)
    nex = chain(islice(nex, 1, None), [None])
    return zip(prev, items, nex)


def execute_ruby_automation(command):
    try:
        os.system(command)
    except:
        pass
