from tkinter import *
from tkinter import scrolledtext
from database import *
from rss_parser import find_info
import pymorphy2
import hyperlink_manager
import webbrowser


# будет главное окно, на котором можно добавить в бд ссылку или удалить ее, добавить ключевое слово или удалить его,
# а также просмотреть текущие списки сайтов и клчевых слов

def insert_link(link):
    add_rss_page(link)


def remove_link(link):
    del_rss_page(link)


def find_news(entry):
    create_table_news()
    app = AppInterface()
    keywords = entry.lower().split()
    new_keywords = []
    for word in keywords:
        morph = pymorphy2.MorphAnalyzer()
        analized_word = morph.parse(word)[0]
        for changed_word in analized_word.lexeme:
            new_keywords.append(changed_word[0])
    pages = get_links_rss_pages()
    for page in pages:
        try:
            find_info(page[0], new_keywords)
        except Exception:
            pass
    print_news_database(app)
    delete_table_news()
    app.show_application()


class BaseAppInterface:
    def __init__(self):
        self.window = self.create_window()
        self.entry_edit_links = Entry(width=15)
        self.entry_keywords = Entry(width=15)
        self.bt_add_links = Button(self.window, text="Добавить источник", width=15, height=3,
                                   command=lambda: insert_link(self.entry_edit_links.get()))
        self.bt_remove_links = Button(self.window, text="Удалить источник", width=15, height=3,
                                      command=lambda: remove_link(self.entry_edit_links.get()))
        self.bt_show_links = Button(self.window, text="Показать источники", width=15, height=3,
                                    command=lambda: print_rss_pages_database())
        self.bt_get_news = Button(self.window, text="Найти новости", width=15, height=3,
                                  command=lambda: find_news(self.entry_keywords.get()))

    def create_window(self):
        window = Tk()
        window.title("Newspaper Controller")
        window.geometry("800x600")
        window.resizable(0, 0)
        window.configure(background='#ffffff')
        return window

    def show_application(self):
        self.bt_add_links.pack()
        self.bt_remove_links.pack()
        self.bt_show_links.pack()
        self.entry_edit_links.pack()
        self.bt_get_news.pack()
        self.entry_keywords.pack()
        self.window.mainloop()


class AppInterface:
    def __init__(self):
        self.window = self.create_window()
        self.txt_field = self.create_scrolled_text()

    def create_window(self):
        window = Tk()
        window.title("Newspaper")
        window.geometry("800x600")
        window.resizable(0, 0)
        window.configure(background='#ffffff')
        return window

    def show_application(self):
        self.txt_field.config(state=DISABLED)
        self.window.mainloop()

    def create_scrolled_text(self):
        txt_field = scrolledtext.ScrolledText(self.window, width=400, height=200)
        txt_field.pack()
        return txt_field

    def edit_scrolled_text(self, text_to_print, link_to_print):
        self.txt_field.insert(INSERT, text_to_print + '  ')
        hyperlink = hyperlink_manager.HyperlinkManager(self.txt_field)
        self.txt_field.insert(INSERT, link_to_print,
                              hyperlink.add(link_to_print))
        self.txt_field.insert(INSERT, '\n\n')

    def get_link(self, link):
        return webbrowser.open(link, new=2)
