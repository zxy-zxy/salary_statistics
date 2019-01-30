from array import array
import time
from datetime import datetime

from api.common import perform_request, predict_rub_salary


def _get_salary_from_superjob_record(record):
    try:
        if record['currency'].lower() != 'rub':
            return 0
        salary_lower_bound = record['payment_from']
        salary_upper_bound = record['payment_to']
        return predict_rub_salary(salary_upper_bound, salary_lower_bound)
    except (KeyError, TypeError):
        return 0


def _parse_records_from_superjob(records):
    result = array('I')
    for record in records:
        result.append(_get_salary_from_superjob_record(record))
    return result


def get_statistics_from_superjob(
        url,
        text,
        total_pages,
        per_page,
        area_code,
        date_from: datetime,
        date_to: datetime,
        token
):
    request_params = dict(
        keyword=text,
        town=area_code,
        date_published_from=time.mktime(date_from.timetuple()),
        date_published_to=time.mktime(date_to.timetuple()),
        count=per_page
    )
    headers = {'X-Api-App-Id': token}

    salary_records = array('I')
    total_records = 0

    for page in range(1, total_pages):
        request_params.update({'page': page})
        response_json = perform_request(url, request_params, headers)

        records = response_json['objects']
        total_records = response_json['total']

        if not records:
            break

        salary_records.extend(_parse_records_from_superjob(records))

    salary_records = list(filter(lambda x: x, salary_records))

    if len(salary_records):
        average_salary = int(sum(salary_records) / len(salary_records))
    else:
        average_salary = 0

    return [text, total_records, len(salary_records), average_salary]