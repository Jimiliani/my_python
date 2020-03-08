from math import sqrt


def for_func():
    for el in [2, 4, 9, 16, 25]:
        print(sqrt(el))


def map_func():
    for el in map(sqrt, [2, 4, 9, 16, 25]):
        print(el)


def list_func():
    print([sqrt(el) for el in [2, 4, 9, 16, 25]])


def main():
    for_func()
    print('\n')
    map_func()
    print('\n')
    list_func()


if __name__ == '__main__':
    main()
