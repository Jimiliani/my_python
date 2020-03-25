temps = {}
with open("stat.txt", "r") as file:
    for line in file:
        line = float(line.strip("\n"))
        try:
            temps[line] += 1
        except KeyError:
            temps[line] = 1
print("Всего уникальных температур: " + str(len(temps)))
print("Средняя температура: " + str(round(sum(temps.keys()) / len(temps), 1)))
print("Максимальная температура: " + str(max(temps.keys())))
print("Минимальная температура: " + str(min(temps.keys())))
