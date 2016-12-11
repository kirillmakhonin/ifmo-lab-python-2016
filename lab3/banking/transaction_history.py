from banking.helpers import get_account
from datetime import datetime
from uuid import uuid4


class Transaction:
    def __init__(self, src_account, trg_account, amount, currency=None, currency_course=None, approved=False, when=None):
        self._src_account = src_account
        self._trg_account = trg_account
        self._amount = amount
        self._when = datetime.now() if when is None else when
        self._id = uuid4()

        if currency:
            self._currency = currency
            self._currency_course = currency_course
            self._approved = approved
        else:
            self._currency = None
            self._currency_course = None
            self._approved = True

    @property
    def id(self):
        return self._id

    @property
    def src_account(self):
        return get_account(self._src_account) if self._src_account else None

    @property
    def src_account_str(self):
        return get_account(self._src_account).__str__(True) if self._src_account else 'BANK'

    @property
    def trg_account(self):
        return get_account(self._trg_account) if self._trg_account else None

    @property
    def trg_account_str(self):
        return get_account(self._trg_account).__str__(True) if self._trg_account else 'BANK'

    def with_client(self, client_id):
        if self._src_account is not None and self.src_account.client._id == client_id:
            return True
        if self._trg_account is not None and self.trg_account.client._id == client_id:
            return True
        return False

    def with_account(self, account_id):
        return self._src_account == account_id or self._trg_account == account_id

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

    @property
    def currency_course(self):
        return self._currency_course

    @property
    def approved(self):
        return self._approved

    @property
    def when(self):
        return self._when

    def approve(self):
        if self.approved:
            return False

        self._approved = True
        self.trg_account.push(self.amount)

    def __str__(self):
        if self._currency is None:
            return "%s Transaction from %s to %s. Amount: %s. Time: %s" % (self.id,
                                                                          self.src_account_str,
                                                                          self.trg_account_str,
                                                                          self.amount,
                                                                          self.when)
        else:
            return "%s Currency transaction from %s to %s. " \
                   "Amount: %s. Time: %s. " \
                   "Currency: %s (course: %s). Approved = %s" % (self.id,
                                                                 self.src_account_str,
                                                                 self.trg_account_str,
                                                                 self.amount,
                                                                 self.when,
                                                                 self.currency,
                                                                 self.currency_course,
                                                                 self.approved)

    @property
    def approved(self) -> bool:
        return self._approved


class TransactionHistory:
    def __init__(self):
        self._transactions = list()

    @property
    def transactions(self) -> list:
        return self._transactions[:]

    def add_transaction(self, transaction: Transaction) -> None:
        self._transactions.append(transaction)

    def find_transaction(self, transaction_id: str) -> Transaction:
        if isinstance(transaction_id, Transaction):
            return transaction_id
        try:
            return next(t for t in self._transactions if t.id == transaction_id)
        except StopIteration:
            return None

    @property
    def unfinished_transactions(self) -> tuple:
        return list(t for t in self._transactions if not t.approved)
