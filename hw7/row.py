def main():
    total = 0
    for num in range(1, 30):
        total += num / (31 - num)
    print(total)


if __name__ == '__main__':
    main()
