from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup


def create_soup(url):
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    return soup


def get_links_from_main_page():
    soup = create_soup("https://viz.berlin.de/aktuelle-meldungen/")
    block_links = soup.find('tbody').find_all('tr')
    current_date = datetime.now().strftime('%d.%m.%Y')
    result = []
    for news in block_links:
        news_date = news.find('td').text
        if news_date == current_date:
            link = "https://viz.berlin.de/" + news.find('a').get('href')
            result.append(link)
        else:
            break
    return result


def open_links(links):
    news = []
    for link in links:
        soup = create_soup(link)
        news_text = soup.find('div', class_='blog-entry').text
        news.append(news_text)
    return news


def get_latest_news():
    return open_links(get_links_from_main_page())
