from datetime import datetime


class Currency:
    """
    Currency class stores information about foreign currences
    """

    def __init__(self, name: str, code: str):
        """
        Create currency
        :param name: Currency name
        :param code: Currency code
        :return:
        """
        self._name = name
        self._code = code.upper()

    def __str__(self):
        return 'Currency: %s. Code: %s' % (self._name, self._code)

    def __repr__(self):
        return 'Currency(%s, %s)' % (self._name, self._code)

    def __hash__(self):
        return hash(self._code)

    @property
    def name(self):
        """
        Get currency name
        :return: str Currency name
        """
        return self._name

    @property
    def code(self):
        """
        Get currency code
        :return: str Currency code
        """
        return self._code


class CurrencyPrice:
    def __init__(self, currency, price, when=None):
        self._currency = currency
        self._price = price
        self._when = datetime.now() if when is None else when

    @property
    def currency(self):
        return self._currency

    @property
    def price(self):
        return self._price

    @property
    def at(self):
        return self._when

    def __str__(self):
        return 'Currency: [%s]. Price: %s (at: %s)' % (self._currency, self._price, self._when)

    def __repr__(self):
        return 'CurrencyPrice(%s, %f, %s)' % (self._currency, self._price, self._when)


class CurrencyPriceArchive:
    def __init__(self, currency_list: tuple = None):
        self._currencies = dict()
        if currency_list is not None:
            for currency in currency_list:
                self.add_currency(currency)

    @property
    def currencies(self):
        return list(self._currencies.keys())

    def get_currency(self, currency):
        if isinstance(currency, Currency):
            return currency
        try:
            return next(c for c in self.currencies if c.code == currency.upper())
        except StopIteration:
            return None

    def add_currency(self, currency: Currency):
        if currency in self._currencies:
            raise Exception("Currency already registered in archive")

        self._currencies[currency] = []

    def get_current_price(self, currency: Currency) -> float:
        if currency not in self._currencies:
            raise Exception("Currency %s is not registered in archive")

        prices = self._currencies[currency]
        if len(prices) == 0:
            return None

        return prices[-1].price

    @property
    def current_prices(self):
        return list(self._currencies[currency][-1]
                    for currency in self.currencies
                    if self.get_current_price(currency) is not None)

    def get_currency_history(self, currency):
        currency = self.get_currency(currency)
        return self._currencies[currency]

    def set_new_price(self, currency: Currency, new_price: float) -> None:
        if currency not in self._currencies:
            raise Exception("Currency %s is not registered in archive")

        self._currencies[currency].append(CurrencyPrice(currency, new_price))