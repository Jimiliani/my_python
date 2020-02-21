def main():
    filmParasites = {12: 250, 16: 350, 20: 450}
    film1917 = {10: 250, 13: 350, 16: 350}
    filmSonik = {10: 350, 14: 450, 18: 450}
    discount = 1.0
    print("Выберите название фильма: ")
    filmName = input()
    print("Выберите день(сегодня, завтра): ")
    filmDay = input()
    print("Выберите время: ")
    filmTime = int(input())
    print("Выберите количество билетов: ")
    countOfTickets = int(input())
    if filmDay == "завтра":
        discount += 0.05
    if countOfTickets >= 20:
        discount += 0.2
    if filmName == "Паразиты":
        try:
            print("Итоговая стоимость: ", discount * filmParasites[filmTime] * countOfTickets)
        except Exception:
            print("Неверно выбрано время")
    elif filmName == "1917":
        try:
            print("Итоговая стоимость: ", discount * film1917[filmTime] * countOfTickets)
        except Exception:
            print("Неверно выбрано время")
    elif filmName == "Соник в кино":
        try:
            print("Итоговая стоимость: ", discount * filmSonik[filmTime] * countOfTickets)
        except Exception:
            print("Неверно выбрано время")
    else:
        print("Такого фильма нет")


if __name__ == "__main__":
    main()
