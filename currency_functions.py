import requests

from currencies import currencies


def get_data():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'

    return requests.get(url).json()


def get_exchange_rates():
    rates = []
    data = get_data()

    for code, name in currencies.items():
        rates.append(f'{name[0]} {code} {data["Valute"][code]["Value"]}')

    result = '\n'.join(rates)

    return result
