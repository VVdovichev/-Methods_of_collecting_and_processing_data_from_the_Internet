'''
Написать приложение, которое собирает основные новости с сайтов mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
'''


from lxml import html
import requests
from fake_headers import Headers
from datetime import datetime


header = Headers(headers=True).generate()


def news_lenta():
    news = []
    keys = ('title', 'date', 'link')
    url_lenta = 'https://lenta.ru/'
    response = requests.get(url_lenta, headers=header)
    root = html.fromstring(response.text)
    root.make_links_absolute(url_lenta)
    news_links = root.xpath('//*[@id="root"]/section[2]/div/div/div[1]/section[1]/div[2]/div/a/@href')

    news_text = root.xpath('//*[@id="root"]/section[2]/div/div/div[1]/section[1]/div[2]/div/a/text()')

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_date = []

    for item in news_links:
        request = requests.get(item)
        root = html.fromstring(request.text)
        date = root.xpath('//time[@class="g-time"]/text()')
        news_date.extend(date)

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value

        news_dict['source'] = 'lenta.ru'
        news.append(news_dict)

    return news


def news_mail():
    news = []
    keys = ('title', 'date', 'link')
    url_mail = 'https://mail.ru/'

    response = requests.get(url_mail, headers=header)
    root = html.fromstring(response.text)

    news_links = root.xpath('//*[@id="index_page"]/div[7]/div[2]/div[1]/div/div[2]/ul/li/a/@href')

    news_text = root.xpath('//*[@id="index_page"]/div[7]/div[2]/div[1]/div/div[2]/ul/li/a/text()')

    for i in range(len(news_text)):
        news_text[i] = news_text[i].replace(u'\xa0', u' ')

    news_links_temp = []
    for item in news_links:
        item = item.split('/')
        news_links_temp.append('/'.join(item[0:5]))

    news_links = news_links_temp

    news_date = []

    for item in news_links:
        request = requests.get(item, headers=header)
        root = html.fromstring(request.text)
        date = root.xpath('//span[contains(@class, "note__text")]/@datetime')
        news_date.extend(date)

    for item in list(zip(news_text, news_date, news_links)):
        news_dict = {}
        for key, value in zip(keys, item):
            news_dict[key] = value
        news_dict['source'] = 'mail.ru'
        news.append(news_dict)
    return news


news_day = news_mail()
news_day.extend(news_lenta())
print(*news_day, sep='\n')
