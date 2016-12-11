from uuid import uuid4


class Client:
    def __init__(self, name: str, bank):
        self._name = name
        self._bank = bank
        self._id = uuid4()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def bank(self):
        return self._name

    def __str__(self):
        return 'Client: %s. ID:%s. Bank: %s [%s]' % (self._name, self._id, self._bank._name, self._bank._id)

    def __repr__(self):
        return 'Client(%s, Bank.find(%s))'

    def open_account(self, currency):
        return self._bank.open_account(self._id, currency)

    def currency_list(self):
        return self._bank.currency_list

    def transfer(self, src_account, trg_account, amount):
        return self._bank.client_transfer(src_account, trg_account, amount, self._id)

    @property
    def accounts(self):
        return self._bank.client_accounts(self._id)

    @property
    def history(self):
        return self._bank.get_client_history(self._id)

    @property
    def full_amount(self):
        return sum(ac.amount_in_rub for ac in self._bank.client_accounts(self._id))

    def get_account_history(self, account_id):
        return self._bank.get_account_history(account_id, self._id)