from uuid import uuid4
from banking.transaction_history import Transaction


class Account:
    def __init__(self, bank, client, amount=0.0, currency=None):
        self._bank = bank
        self._client = client
        self._id = uuid4()
        self._amount = amount
        self._currency = currency

        if self._amount < 0:
            raise Exception("Cannot open account with negative amount")

        if self._amount != 0:
            current_currency_price = bank.get_currency_price(currency) if currency is not None else 0
            bank.add_transaction(Transaction(None, self._id, amount, currency, current_currency_price, True))

    @property
    def amount(self):
        return self._amount

    @property
    def amount_in_rub(self):
        if self._currency is None:
            return self._amount
        else:
            return self._bank.get_currency_price(self._currency) * self._amount

    @property
    def bank(self):
        return self._bank

    @property
    def client(self):
        return self._client

    @property
    def id(self):
        return self._id

    @property
    def currency(self):
        return self._currency

    def __str__(self, short=False):
        if short:
            return "%s's account in %s bank" % (self.client.name, self.bank.name)
        return "%s's account in %s bank. Amount: %s. Currency: %s" % (self.client.name, self.bank.name, self.amount, self.currency if self.currency else '-')

    def pull(self, amount):
        if amount <= 0:
            raise Exception("Cannot pull negative amount")

        if self._amount < amount:
            raise Exception("Not enought amount on account")

        self._amount -= amount
        return True

    def push(self, amount):
        if amount <= 0:
            raise Exception("Cannot push negative amount")

        self._amount += amount
        return True

    def transfer(self, target_account, amount):
        return self._bank.client_transfer(self, target_account, amount)

