from collections import namedtuple

Task = namedtuple("task", "time category text")

todo_list = []


def mainloop():
    command = ""
    while True:
        command = input().lower()
        if command == "add":
            task = Task(input(), input(), input())
            todo_list.append(task)
        elif command == "print":
            counter = 0
            for task in todo_list:
                counter += 1
                print(counter, task[0], task[1], task[2])
        elif command == "end":
            break
        else:
            print("Unknown command")


if __name__ == '__main__':
    mainloop()
