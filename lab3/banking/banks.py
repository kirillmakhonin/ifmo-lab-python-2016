from uuid import uuid4
from banking.helpers import *
from banking.transaction_history import (TransactionHistory, Transaction)
from banking.currency import (Currency, CurrencyPriceArchive)
from banking.client import Client
from banking.accounting import Account


class Bank:
    def __init__(self, name, id=None):
        self._name = name
        self._id = uuid4() if id is None else id
        self._transactions = TransactionHistory()
        self._accounts = dict()
        self._clients = dict()
        self._currency_prices = CurrencyPriceArchive()

        BankStorage[self._id] = self

    # general
    def __str__(self):
        return "Bank: %s. Id: %s" % (self._name, self._id)

    def __repr__(self):
        return "Bank('%s', '%s')" % (self._name, self._id)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name
    # / general

    # clients
    def add_client(self, name):
        client = Client(name, bank=self)
        self._clients[client._id] = client
        return client

    @property
    def clients(self):
        return list(self._clients.values())

    def get_client(self, client):
        if isinstance(client, Client):
            return client

        return self._clients.get(client)

    # / clients

    # accounts
    @property
    def accounts(self):
        return list(self._accounts.values())

    def get_account(self, account_id):
        if isinstance(account_id, Account):
            return account_id

        return self._accounts.get(account_id)

    def add_account(self, client_id, amount=0, currency=None):
        client = self.get_client(client_id)
        currency = self.get_currency(currency) if currency is not None else None
        account = Account(self, client, amount, currency)
        self._accounts[account._id] = account
        return account

    def client_accounts(self, initiator_id):
        return list(ac for ac in self.accounts if ac.client.id == initiator_id)

    def get_client_history(self, initiator_id):
        return list(tr for tr in self._transactions.transactions if tr.with_client(initiator_id))

    def get_account_history(self, account_id):
        return list(tr for tr in self._transactions.transactions if tr.with_account(account_id))

    @property
    def full_amount(self):
        return sum(ac.amount_in_rub for ac in self._accounts.values())

    # / accounts

    # transactions

    def add_transaction(self, transaction: Transaction) -> None:
        self._transactions.add_transaction(transaction)

    def get_transaction(self, transaction_id) -> Transaction:
        return self._transactions.find_transaction(transaction_id)

    @property
    def transactions(self) -> list:
        return self._transactions.transactions

    @property
    def unapproved_transactions(self) -> list:
        return self._transactions.unfinished_transactions

    def client_transfer(self, src_account, trg_account, amount):
        src, trg = get_account(src_account), get_account(trg_account)
        if src is None or trg is None:
            raise Exception("Cannot find all accounts")

        # pull money
        src.pull(amount)

        if src.currency is None and trg.currency is None:
            trg.push(amount)
            transaction = Transaction(src.id, trg.id, amount)
        else:
            if src.currency is not None and \
                trg.currency is not None and \
                            src.currency != trg.currency:
                raise Exception("Cannot convert between different currencies")

            if src.currency == trg.currency:
                currency = src.currency
                course = self.get_currency_price(currency)
                new_amount = amount
            elif src.currency is not None:
                currency = src.currency
                course = self.get_currency_price(currency)
                new_amount = amount * course
            else:
                currency = src.currency
                course = self.get_currency_price(currency)
                new_amount = amount / course
            transaction = Transaction(src.id, trg.id, new_amount, currency, course)

        self.add_transaction(transaction)
        return transaction

    # / transactions

    # currencies

    @property
    def currency_list(self):
        return self._currency_prices.currencies

    def get_currency(self, currency):
        return self._currency_prices.get_currency(currency)

    def get_currency_price(self, currency):
        return self._currency_prices.get_current_price(currency)

    def add_currency(self, currency: Currency):
        self._currency_prices.add_currency(currency)
        return currency

    def set_currency_price(self, currency: Currency, new_price: float):
        self._currency_prices.set_new_price(self._currency_prices.get_currency(currency), new_price)

    @property
    def current_currencies(self):
        return self._currency_prices.current_prices

    def get_currency_history(self, currency):
        return self._currency_prices.get_currency_history(currency)

    # / currencies

    @staticmethod
    def find(bank_id):
        return BankStorage.get(bank_id)

