def numeric(name):
    try:
        with open(name, "r") as file:
            with open("update_" + name, "w") as updated_file:
                n = 0
                for line in file:
                    n += 1
                    updated_file.write(str(n) + ' ' + line)
    except FileNotFoundError:
        print("Неверно указан файл")


numeric("abc")
numeric("moby.txt")
