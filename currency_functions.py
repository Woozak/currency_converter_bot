import requests

from currencies import currencies


def is_number(message):
    value = message.text.replace(',', '.')
    try:
        return float(value) > 0
    except ValueError:
        return False


def get_data():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'

    result = requests.get(url).json()
    result['Valute']['RUB'] = {"Nominal": 1, 'Value': 1}

    return result


def get_value(code, data):

    return data["Valute"][code]["Value"] / data["Valute"][code]["Nominal"]


def get_exchange_rates():
    rates = []
    data = get_data()

    for code, name in currencies.items():
        if code == 'RUB':
            continue
        value = round(get_value(code, data), 3)
        rates.append(f'{name[0]} {code} = {value} RUB')

    result = '\n'.join(rates)

    return result


def currency_converter(first, second, quantity):
    data = get_data()

    first_value = get_value(first, data)
    second_value = get_value(second, data)
    result = round(first_value / second_value * quantity, 3)

    return f'{quantity} {currencies[first][0]} {first} = {result} {currencies[second][0]} {second}'
