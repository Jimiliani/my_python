from tkinter import *
import sqlite3


def create_table():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    try:
        cursor.execute(""" CREATE TABLE tasks
            (task_ text,
            category_ text,
            time_ text)
            """)
        conn.commit()
    except Exception:
        pass
    conn.close()


def write_order(data):
    connection = sqlite3.connect('tasks.db')
    curs = connection.cursor()
    curs.execute("INSERT INTO tasks VALUES (?,?,?)", (data['task'], data['category'], data['time']))
    connection.commit()
    connection.close()


def order():
    data = {
        'task': entry_task.get(),
        'category': entry_category.get(),
        'time': entry_time.get()
    }
    write_order(data)


def print_tasks():
    connection = sqlite3.connect('tasks.db')
    curs = connection.cursor()
    curs.execute("SELECT * FROM tasks")
    for row in curs.fetchall():
        line = 'Задача:' + row[0] + '  Категория:' + row[1] + '  Дата:' + row[2] + '\n'
        txt_field.insert(1.0, line)
    txt_field.insert(1.0, '\n')
    connection.commit()
    connection.close()


# except Exception:
#     print("Ошибка при работе с базой данных")
#     exit(1)


def end():
    exit(0)


create_table()
window = Tk()
window.title("Менеджер задач")
Label(text="Задача:").grid(row=0, column=0, pady=2, padx=5)
Label(text="Категория:").grid(row=1, column=0, pady=2, padx=5)
Label(text="Время:").grid(row=2, column=0, pady=2, padx=5)
entry_task = Entry()
entry_task.grid(row=0, column=1, columnspan=2, padx=5)
entry_category = Entry()
entry_category.grid(row=1, column=1, columnspan=2, padx=5)
entry_time = Entry()
entry_time.grid(row=2, column=1, columnspan=2, padx=5)
btn_order = Button(text="Заказать", command=order).grid(row=3, column=1)
btn_task_list = Button(text="Список задач", command=print_tasks).grid(row=4, column=1)
btn_exit = Button(text="Выход", command=end).grid(row=5, column=1)
txt_field = Text(window, width=40, height=10)
txt_field.grid(row=0, column=4, columnspan=1, rowspan=6, padx=5, pady=3)
window.mainloop()
