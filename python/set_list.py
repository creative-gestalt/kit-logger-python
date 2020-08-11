some_list = []

with open('C:\\Users\\thebb\\github\\kit-logger-ruby\\data\\used\\used_location_ids.txt', 'r') as f:
    for line in f:
        some_list.append(line)


uniq = set(some_list)

with open('C:\\Users\\thebb\\github\\kit-logger-ruby\\data\\used\\used_location_ids.txt', 'w') as f:
    for item in some_list:
        f.write('%s' % item)
