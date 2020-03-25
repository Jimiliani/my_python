with open("moby_clean.txt", "r") as file:
    di = {}
    for line in file:
        line = line.strip('\n')
        if line == '':
            continue
        di.setdefault(line, 0)
        di[line] += 1
    swapped_dict = dict([(value, key) for key, value in di.items()])
    keys = sorted(swapped_dict.keys(), reverse=True)
    for i in range(5):
        print(swapped_dict[keys[i]])
