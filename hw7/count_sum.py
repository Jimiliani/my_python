def main():
    num = input()
    total = 0
    for digit in num:
        if int(digit) % 2 != 0:
            total += int(digit)**2
    print(total)


if __name__ == '__main__':
    main()