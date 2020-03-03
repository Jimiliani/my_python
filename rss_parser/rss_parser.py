import urllib
from database import add_news
from urllib.request import urlopen
from bs4 import BeautifulSoup


def find_info(link, keyword):
    page = urllib.request.urlopen(link)
    soup = BeautifulSoup(page, features="html.parser")
    all_items = soup.findAll('item')
    print_info(all_items, keyword)


def print_link(item, normal_title):
    link_list = item.findAll('guid')
    for html_link in link_list:
        for normal_link in html_link:
            add_news(normal_title, normal_link)


def print_info(list_of_items, keyword):
    for item in list_of_items:
        title_list = item.findAll('title')
        for html_title in title_list:
            for normal_title in html_title:
                if any(word in normal_title.lower() for word in keyword):
                    print_link(item, normal_title)
