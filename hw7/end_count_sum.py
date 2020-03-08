def main():
    total = 0
    while True:
        num = input()
        try:
            num = int(num)
            total += num
        except Exception:
            if num == "Стоп":
                break
            print("Некорректный ввод, попробуйте снова")
    print(total)


if __name__ == '__main__':
    main()
