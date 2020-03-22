import csv


def csv_reader(file):
    reader = csv.reader(file)
    for row in reader:
        print(row)


def csv_writer(file, row):
    writer = csv.writer(file)
    writer.writerow(row)
