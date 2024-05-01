import requests


def get_data():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'

    return requests.get(url).json()

