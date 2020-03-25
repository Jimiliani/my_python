import csv


def make_csv(filename, list_):
    with open(filename, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(['name', 'address', 'age'])
        for line in list_:
            writer.writerow(list(line))


make_csv("aaa.csv", [('Георгий', 'Невский проспект', '22'), ('Иван', 'пр.Ветеранов', '21')])
