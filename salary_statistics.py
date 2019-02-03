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

    HH_RECORDS_PER_PAGE_TO_PROCESS = 100
    SUPERJOB_RECORDS_PER_PAGE_TO_PROCESS = 10

    hh_moscow_area_code = 1
    superjob_moscow_area_code = 4
    days_to_review = 30

    specializations = [
        'Программист Python',
        'Программист Java',
        'Программист C++',
        'Программист JavaScript',
    ]

    headers = [
        'Специализация',
        'Всего записей',
        'Всего обработанных записей',
        'Средняя зарплата'
    ]

    table_data = [headers]

    table_data.append(['HH.ru'])

    for specialization in specializations:
        try:
            statistics_from_hh = get_statistics_from_hh(
                HEADHUNTER_URL,
                specialization,
                HH_RECORDS_PER_PAGE_TO_PROCESS,
                hh_moscow_area_code,
                days_to_review
            )
            table_data.append(statistics_from_hh.values())
        except SalaryAPIException as e:
            sys.exit(e)

    table_data.append(['Superjob.ru'])

    for specialization in specializations:
        try:
            statistics_from_superjob = get_statistics_from_superjob(
                SUPERJOB_URL,
                specialization,
                SUPERJOB_RECORDS_PER_PAGE_TO_PROCESS,
                superjob_moscow_area_code,
                days_to_review,
                token=SUPERJOB_TOKEN
            )
        except SalaryAPIException as e:
            sys.exit(e)
        table_data.append(statistics_from_superjob.values())

    table = AsciiTable(table_data)
    print(table.table)
