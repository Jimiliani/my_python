import csv


def read_csv(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        keys, ans = [], []
        dict_ = {}
        first_line = True
        for line in reader:
            if first_line:
                for word in line:
                    keys.append(word)
                first_line = False
                continue
            i = 0
            for word in line:
                dict_[keys[i]] = word
                i += 1
            ans.append(dict_)
        return ans


print(read_csv('aaa.csv'))
