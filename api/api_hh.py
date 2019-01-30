from array import array

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


def get_statistics_from_hh(url, text, total_pages, per_page, area, date_from, date_to):
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

    for page in range(1, total_pages):
        request_params.update({'page': page})
        response_json = perform_request(url, request_params)

        records = response_json['items']
        total_records = response_json['found']

        if not records:
            break

        salary_records.extend(_parse_records_from_hh(records))

    salary_records = list(filter(lambda x: x, salary_records))

    if len(salary_records):
        average_salary = int(sum(salary_records) / len(salary_records))
    else:
        average_salary = 0

    return [text, total_records, len(salary_records), average_salary]
