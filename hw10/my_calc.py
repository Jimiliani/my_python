while True:
    x, y = 0, 0
    try:
        print("Введите 2 числа")
        try:
            x, y = input().split()
        except ValueError:
            print("Слишком много или слишком мало аргументов, попробуйте снова")
            continue
        x, y = float(x), float(y)
    except ValueError:
        print("Неверно введены числа, попробуйте снова")
        continue

    print("Введите знак")
    s = input()
    if s == "+":
        print(x + y)
    elif s == "-":
        print(x - y)
    elif s == "*":
        print(x * y)
    elif s == "/":
        try:
            print(x / y)
        except ZeroDivisionError:
            print("На ноль делить нельзя, попробуйте снова")
            continue
    else:
        print("Неверно введен знак, попробуйте снова")
        continue
