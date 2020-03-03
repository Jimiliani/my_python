import sqlite3
from tkinter import messagebox


def create_table_rss_pages():
    try:
        connection = sqlite3.connect('rss_pages.db')
        curs = connection.cursor()
        curs.execute(""" CREATE TABLE rss_pages
                    (link text)""")
        connection.commit()
        connection.close()
    except Exception:
        pass


def create_table_news():
    try:
        connection = sqlite3.connect('news.db')
        curs = connection.cursor()
        curs.execute(""" CREATE TABLE news
                    (title text,
                     link text)""")
        connection.commit()
        connection.close()
    except Exception:
        pass


def delete_table_news():
    connection = sqlite3.connect('news.db')
    curs = connection.cursor()
    curs.execute("""DROP TABLE news""")
    connection.commit()
    connection.close()


def add_rss_page(link_):
    connection = sqlite3.connect("rss_pages.db")
    curs = connection.cursor()
    curs.execute("INSERT INTO rss_pages VALUES (?)", (link_,))
    connection.commit()
    connection.close()


def add_news(title_, link_):
    connection = sqlite3.connect("news.db")
    curs = connection.cursor()
    curs.execute("SELECT * FROM news WHERE link = ?", (link_,))
    if len(curs.fetchall()) == 0:
        curs.execute("INSERT INTO news VALUES (?,?)", (title_, link_))
    connection.commit()
    connection.close()


def del_news(title_, link_):
    connection = sqlite3.connect('news.db')
    curs = connection.cursor()
    curs.execute("DELETE FROM news WHERE (title = ?, link = ?)", (title_, link_))
    connection.commit()
    connection.close()


def del_rss_page(link_):
    connection = sqlite3.connect('rss_pages.db')
    curs = connection.cursor()
    curs.execute("DELETE FROM rss_pages WHERE (link = ?)", (link_,))
    connection.commit()
    connection.close()


def print_news_database(app):
    connection = sqlite3.connect('news.db')
    curs = connection.cursor()
    curs.execute("SELECT * FROM news")
    for row in curs.fetchall():
        app.edit_scrolled_text(row[0], row[1])
    connection.close()


def print_rss_pages_database():
    connection = sqlite3.connect('rss_pages.db')
    curs = connection.cursor()
    text_message = ""
    curs.execute("SELECT * FROM rss_pages")
    for link in curs.fetchall():
        text_message += str(link[0]) + '\n'
    messagebox.showinfo("Источники", text_message)
    connection.close()


def get_links_rss_pages():
    connection = sqlite3.connect('rss_pages.db')
    curs = connection.cursor()
    curs.execute("SELECT * FROM rss_pages")
    links = []
    for link in curs.fetchall():
        links.append(link)
    connection.close()
    return links
