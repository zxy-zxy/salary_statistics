import datetime
from array import array
from itertools import count

from api.common import perform_request, predict_rub_salary


def _get_salary_from_hh_record(record):
    try:
        salary_element = record['salary']
        if salary_element['currency'].lower() != 'rur':
            return 0
        salary_lower_bound = salary_element['from']
        salary_upper_bound = salary_element['to']
        return predict_rub_salary(salary_upper_bound, salary_lower_bound)
    except (KeyError, TypeError):
        return 0


def _parse_records_from_hh(records):
    result = array('I')
    for record in records:
        result.append(_get_salary_from_hh_record(record))
    return result


def get_statistics_from_hh(url, text, per_page, area, days_to_review):
    date_to = datetime.datetime.now()
    date_from = \
        datetime.datetime.now() - datetime.timedelta(days=days_to_review)

    request_params = dict(
        text=text,
        area=area,
        date_from=date_from.strftime("%Y-%m-%d"),
        date_to=date_to.strftime("%Y-%m-%d"),
        per_page=per_page,
        describe_arguments=True
    )
    salary_records = array('I')
    total_records = 0

    for page in count(start=1):
        request_params.update({'page': page})
        response_json = perform_request(url, request_params)
        pages_count = response_json['pages']
        if page > pages_count:
            break

        records = response_json['items']
        total_records = response_json['found']

        salary_records.extend(_parse_records_from_hh(records))

    salary_records = [x for x in salary_records if x]

    if len(salary_records):
        average_salary = int(sum(salary_records) / len(salary_records))
    else:
        average_salary = 0

    return {
        'specialization': text,
        'total_records': total_records,
        'processed_records':
            len(salary_records),
        'average_salary': average_salary
    }
