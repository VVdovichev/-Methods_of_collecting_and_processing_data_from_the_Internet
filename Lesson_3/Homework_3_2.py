'''
Написать функцию, которая производит поиск и выводит на экран вакансии с
заработной платой больше введённой суммы.
'''


import pandas as pd
from pymongo import MongoClient


CROSS = {'USD': 73.07}


def recalculate_salary(row):
    return row.min_salary if row.currency not in CROSS.keys() else float(row.min_salary) * CROSS[row.currency]


def filter_vacancies(**kwargs):
    db_host = kwargs.get('host', 'mongodb://localhost:27017/')
    db_name = kwargs.get('database', 'GB_Homework')
    collection_name = kwargs.get('collection', 'Vacancies')
    base_currency = kwargs.get('currency', 'руб.')
    minimal_salary = kwargs.get('minimal_salary', 90000)

    # get database and collection
    client = MongoClient(db_host)
    db = client[db_name]
    collection = db[collection_name]

    # request to MongoDB
    query = collection.find(filter={'min_salary': {'$ne': ''}, 'currency': {'$ne': ''}},
                            projection={'_id': 1, 'min_salary': 1, 'currency': 1})
    data = list(query)

    # cast to DataFrame and recalculate salaries if required
    df = pd.DataFrame(data)
    cond = df['currency'] != base_currency
    df.loc[cond, 'min_salary'] = df.loc[cond, ['min_salary', 'currency']].apply(recalculate_salary, axis=1)

    ids = df.loc[df['min_salary'].astype('float') > minimal_salary, '_id']

    # get full info about vacancies from MongoDB
    query = collection.find(filter={'_id': {'$in': ids.tolist()}}, projection={'_id': 0})
    data = list(query)
    df = pd.DataFrame(data)
    df.to_csv('vacancies_filtered.csv')


filter_vacancies(minimal_salary=90000)
