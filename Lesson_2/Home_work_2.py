"""
Вариант 1
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы) с сайтов
Superjob и HH. Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
Наименование вакансии.
Предлагаемую зарплату (отдельно минимальную и максимальную).
Ссылку на саму вакансию.
Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas.
"""


import requests
import re
import pandas as pd
from fake_headers import Headers
from bs4 import BeautifulSoup as bs
import lxml


URL_HH = 'https://hh.ru/search/vacancy'
URL_SJ = 'https://www.superjob.ru/vacancy/search/'
df_cols = ['Title', 'Salary (min)', 'Salary (max)', 'Currency', 'Link', 'Source']
vacancy = 'Data scientist'      # job title
pages = int(input('Введите кол-во страниц для парсера: '))


def parse_salary(salaries):
    """ Parse salaries to min/max"""
    # parse salaries: min/max
    min_salaries, max_salaries = [], []
    for sal in salaries:
        regex = re.findall(r'(\d+)', sal)
        if len(regex) > 1:
            min_salaries.append(regex[0])
            max_salaries.append(regex[1])
        elif len(regex) > 0:
            if sal.find(u'от') != -1:
                min_salaries.append(regex[0])
                max_salaries.append('')
            else:
                min_salaries.append('')
                max_salaries.append(regex[0])
        else:
            min_salaries.append('')
            max_salaries.append('')
    return min_salaries, max_salaries


def parse_hh_page(pg_num: int, **kwargs):
    """ Parse one page on HeadHunter site """
    home_url = 'https://hh.ru'
    hdr = kwargs.get('header', Headers(headers=True).generate())
    vcn = kwargs.get('vacancy', '')
    vacancy_param = {'text': vcn, 'page': pg_num}

    # request to HeadHunter
    response = requests.get(URL_HH, params=vacancy_param, headers=hdr)
    # parsing
    soup = bs(response.text, 'lxml')

    vacancy_headers = [elem for elem in soup.find_all(class_='vacancy-serp-item__row_header')]
    titles = [elem.find(class_='resume-search-item__name').text for elem in vacancy_headers]
    links = [url.get('href') for elem in vacancy_headers for url in elem('a')]
    salaries = [salary.text.replace('\u202f', '') if (salary := elem.find(class_='vacancy-serp-item__sidebar')) else ''
                for elem in vacancy_headers]
    currencies = [spl[-1] if (spl := cur.split()) else '' for cur in salaries]

    # parse salaries: min/max
    min_salaries, max_salaries = parse_salary(salaries)

    return pd.DataFrame([titles, min_salaries, max_salaries, currencies, links, [home_url] * len(titles)],
                        index=df_cols).T


def parse_sj_page(pg_num: int, **kwargs):
    """ Parse one page on SuperJob site """
    home_url = 'https://www.superjob.ru'
    hdr = kwargs.get('header', Headers(headers=True).generate())
    vcn = kwargs.get('vacancy', '')
    vacancy_param = {'keywords': vcn, 'page': pg_num}

    # request to SuperJob
    response = requests.get(URL_SJ, params=vacancy_param, headers=hdr)
    # parsing
    soup = bs(response.text, 'lxml')
    titles = [elem.text for elem in soup.find_all(class_='_6AfZ9')]
    links = [f'{home_url}{elem.get("href")}' for elem in soup.find_all(class_='_6AfZ9')]
    salaries = [elem.text.replace('\xa0', '') for elem in soup.find_all(class_=['_1qw9T'])]
    currencies = [regex.group(1) if (regex := re.search(r'\d(\D+)/', cur)) else '' for cur in salaries]

    # parse salaries: min/max
    min_salaries, max_salaries = parse_salary(salaries)

    return pd.DataFrame([titles, min_salaries, max_salaries, currencies, links, [home_url] * len(titles)],
                        index=df_cols).T


header = Headers(headers=True).generate()
df = pd.DataFrame(columns=df_cols)
for pg in range(pages):
    df = df.append(parse_sj_page(pg, header=header, vacancy=vacancy), ignore_index=True)
    df = df.append(parse_hh_page(pg, header=header, vacancy=vacancy), ignore_index=True)

df.drop_duplicates(inplace=True, ignore_index=True)
df.index = df.index + 1
df.to_csv('vacancies.csv')

