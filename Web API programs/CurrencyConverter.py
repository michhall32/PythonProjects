from requests import get
from pprint import PrettyPrinter
from datetime import date


BASE_URL = 'https://api.nbp.pl/api/exchangerates/'

printer = PrettyPrinter()

def get_currencies():
    endpoint = 'tables/a/'
    data = get(BASE_URL + endpoint).json() 
    currencies = data[0]['rates']
    return currencies


def print_currencies(currencies):
    for i, currency in enumerate(currencies):
        print(f"{i+1:2}. {currency['code']} - {currency['currency']}")


def avaiableCurrenciesList(currencies):
    avaiableCurrencies = []
    for currency in currencies:
        avaiableCurrencies.append(currency['code'])

    return avaiableCurrencies


def exchange_rate(currency, date=date.today()):
    endpoint = f'rates/a/{currency}/{date}'
    url = BASE_URL + endpoint
    try:
        data = get(url).json()
        rate = data["rates"][0]['mid']
        print(f"\n1 {currency.upper()} = {rate} PLN")
        return rate
    except ValueError as E:
        print(f'Invalid date. More details: {E}')
        return


def convert(currency, amount, availableList, date=date.today()):

    try:
        amount = abs(float(amount))
    except ValueError as E:
        print(f'Invalid amount. More details: {E}')
        return

    if currency in availableList:
        rate = exchange_rate(currency, date)
        if rate is None:
            return
        else:
            converted_amount = rate * amount
            print(f'{amount} {currency} = {converted_amount} PLN')
    else:
        print('Currency not valid or unavailable.')
        return

    return converted_amount


def main():
    currencies = get_currencies()
    avaiableCurrencies = avaiableCurrenciesList(currencies)
    print('----------CURRENCY CONVERTER-----------')
    print('1 - List of different currencies')
    print('2 - Convert a currency to PLN')
    print('3 - Historical convert rate')

    while True:
        command = input('\nEnter a command (q to quit): ').lower()
        if command == 'q':
            break
        elif command == '1':
            print_currencies(currencies)
        elif command == '2':
            currency = input('Enter a currency id: ').upper()
            amount = input('Enter an amount: ')
            convert(currency, amount, avaiableCurrencies)
        elif command == '3':
            date = input('Enter a weekday (RRRR-MM-DD): ')
            currency = input('Enter a currency id: ').upper()
            amount = input('Enter an amount: ')
            convert(currency, amount, avaiableCurrencies, date)
        else:
            print('Unrecognised command!')


main()


