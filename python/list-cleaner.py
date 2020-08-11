from collections import OrderedDict
from pathlib import Path

cities = Path('./states/arizona/city.txt')
_dict = Path('./states/arizona/city-dictionary.txt')


def remove_dups(file):
    some_list = []
    with open(file) as f:
        for line in f:
            some_list.append(line.rstrip())
    new_list = list(OrderedDict.fromkeys(some_list))
    with open(file, 'w') as f:
        for item in new_list:
            f.write('%s\n' % item)


def sort_list(file):
    some_list = []
    with open(file) as f:
        for line in f:
            some_list.append(line.rstrip().replace(' ', '_'))
    some_list.sort()
    with open(file, 'w') as f:
        for item in some_list:
            f.write('%s\n' % item)


def sort_list_from_second_value(file):
    some_list = []
    with open(file) as f:
        for line in f:
            some_list.append(line.rstrip())
    some_list.sort(key=lambda s: s.split()[1])
    with open(file, 'w') as f:
        for item in some_list:
            f.write('%s\n' % item)


# sort_list_from_second_value(_dict)
# sort_list(cities)
# remove_dups(cities)
