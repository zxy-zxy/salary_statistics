# Salary statistics for open positions
### This script showing statistics for open positions from [HH.ru](https://hh.ru/) and [Superjob](https://www.superjob.ru/)

## Requirements
Python >= 3.5 required.  
Install dependencies with 
```bash
pip install -r requirements.txt
```
For better interaction is recommended to use [virtualenv](https://github.com/pypa/virtualenv).

## Usage
[HH.ru](https://hh.ru/) Does not required any special auth token, but 
[Superjob](https://www.superjob.ru/) does. 
Create .env file and store **Superjob** auth token as ***superjob_api_token***. 

Script will analyze all vacancies for last 30 days in Moscow with Russian ruble as currency.
As of now following specialities considering:
* Java programmer
* Python programmer
* JavaScript programmer
* C++ programmer

Run script:
```bash
python salary_statistics.py
```

## Output
```bash
+------------------------+---------------+----------------------------+------------------+---+
| Специализация          | Всего записей | Всего обработанных записей | Средняя зарплата |   |
+------------------------+---------------+----------------------------+------------------+---+
| HH.ru                  |               |                            |                  |   |
| Программист Python     | 1287          | 320                        | 143568           |   |
| Программист Java       | 1594          | 374                        | 157746           |   |
| Программист C++        | 178           | 26                         | 138346           |   |
| Программист JavaScript | 2393          | 759                        | 127729           |   |
| Superjob.ru            |               |                            |                  |   |
| Программист Python     | 14            | 3                          | 111666           |   |
| Программист Java       | 35            | 5                          | 169800           |   |
| Программист C++        | 29            | 13                         | 74830            |   |
| Программист JavaScript | 47            | 21                         | 89790            |   |
+------------------------+---------------+----------------------------+------------------+---+
```