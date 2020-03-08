def main():
    mass = float(input())
    print("Месяц Вес")
    for month in range(1, 6):
        print(" ", month, " ", mass - month * 1.5)


if __name__ == '__main__':
    main()
