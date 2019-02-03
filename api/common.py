import requests


class SalaryAPIException(Exception):
    pass


def perform_request(url, request_params, headers=None):
    try:
        response = requests.get(
            url,
            params=request_params,
            headers=headers
        )
    except requests.exceptions.RequestException as e:
        raise SalaryAPIException(
            f'An error has occurred during request: {e}'
        )

    if not response.ok:
        raise SalaryAPIException(
            '''
            A response from HH is not ok:
            code: {}
            text: {}
            '''.format(response.status_code, response.text)
        )

    try:
        response_json = response.json()
    except ValueError as e:
        raise SalaryAPIException(
            f'A response from HH cannot be parsed properly: {e}'
        )

    return response_json


def predict_rub_salary(salary_upper_bound, salary_lower_bound):
    if salary_upper_bound and salary_lower_bound:
        return int((salary_lower_bound + salary_upper_bound) / 2)
    elif salary_lower_bound:
        return int(salary_lower_bound * 1.2)
    else:
        return int(salary_upper_bound * 0.8)
