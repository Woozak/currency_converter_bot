import requests

from currencies import currencies


def get_data():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'

    return requests.get(url).json()


def get_value(code):
    data = get_data()

    return data["Valute"][code]["Value"] / data["Valute"][code]["Nominal"]


def get_exchange_rates():
    rates = []

    for code, name in currencies.items():
        if code == 'RUB':
            continue
        value = round(get_value(code), 3)
        rates.append(f'{name[0]} {code}  {value}')

    result = '\n'.join(rates)

    return result


def currency_converter(first, second, quantity):
    first_value = get_value(first)
    second_value = get_value(second)
    result = round(first_value / second_value, 3) * quantity

    return f'{quantity} {currencies[first][0]} {first} = {result} {currencies[second][0]} {second}'
