from interface import *


def main():
    create_table_rss_pages()
    base_app = BaseAppInterface()
    base_app.show_application()


# ссылку лучше сделать прям на буквах, чтобы можно было нажать и попасть на сайт, а то ссылки мешаются

# когда будет готов интерфейс надо добавить сохранение для списка сайтов на которых поиск делаем


if __name__ == '__main__':
    main()
