from . import logger
import os
from pathlib import Path
from halo import Halo

start_num = None
end_num = None


def generate_card_numbers(user, start_num, end_num):
    member_numbers = []
    path = Path(f'./user_member_numbers/{user}/')
    if not os.path.exists(path):
        os.makedirs(path)
    member_file = Path(f'./user_member_numbers/{user}/member_numbers.txt')
    start = int(start_num)
    end = int(end_num)
    difference = (end - start) + 1
    if difference > 101:
        message = 'Kit count exceeded 100, make sure that\'s what you intended'
        print(message)
    for num in range(difference):
        member_numbers.append(start)
        start += 1
    with open(member_file, 'w') as m:
        for item in member_numbers:
            m.write('%s\n' % item)
    print('Numbers generated')
    return member_numbers


if __name__ == "__main__":
    generate_card_numbers(start_num=start_num, end_num=end_num)
