import datetime
import sys
import os

from terminaltables import AsciiTable
from dotenv import load_dotenv

from api.api_hh import get_statistics_from_hh
from api.api_superjob import get_statistics_from_superjob
from api.common import SalaryAPIException

if __name__ == '__main__':
    load_dotenv()

    SUPERJOB_TOKEN = os.getenv('superjob_api_token')
    HEADHUNTER_URL = 'https://api.hh.ru/vacancies'
    SUPERJOB_URL = 'https://api.superjob.ru/2.0/vacancies'

    PAGES_TO_PROCESS = 20
    HH_RECORDS_PER_PAGE_TO_PROCESS = 100
    SUPERJOB_RECORDS_PER_PAGE_TO_PROCESS = 10

    hh_moscow_area_code = 1
    superjob_moscow_area_code = 4

    vacancies = [
        'Программист Python',
        'Программист Java',
        'Программист C++',
        'Программист JavaScript',
    ]

    header = [
        'Профессия',
        'Всего записей',
        'Всего обработанных записей',
        'Средняя зарплата'
    ]

    table_data = [header]

    table_data.append(['HH.ru'])

    for vacancy in vacancies:
        try:
            statistics_from_hh = get_statistics_from_hh(
                HEADHUNTER_URL,
                vacancy,
                PAGES_TO_PROCESS,
                HH_RECORDS_PER_PAGE_TO_PROCESS,
                hh_moscow_area_code,
                datetime.datetime.now() - datetime.timedelta(days=30),
                datetime.datetime.now()
            )
            table_data.append(statistics_from_hh)
        except SalaryAPIException as e:
            sys.exit(e)

    table_data.append(['Superjob.ru'])

    for vacancy in vacancies:
        try:
            statistics_from_superjob = get_statistics_from_superjob(
                SUPERJOB_URL,
                vacancy,
                PAGES_TO_PROCESS,
                SUPERJOB_RECORDS_PER_PAGE_TO_PROCESS,
                superjob_moscow_area_code,
                datetime.datetime.now() - datetime.timedelta(days=30),
                datetime.datetime.now(),
                token=SUPERJOB_TOKEN
            )
        except SalaryAPIException as e:
            sys.exit(e)
        table_data.append(statistics_from_superjob)

    table = AsciiTable(table_data)
    print(table.table)
