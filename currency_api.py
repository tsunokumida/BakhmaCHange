from currency_converter import CurrencyConverter

converter = CurrencyConverter()

def convert_currency(amount, from_currency, to_currency):
    return converter.convert(amount, from_currency, to_currency)
