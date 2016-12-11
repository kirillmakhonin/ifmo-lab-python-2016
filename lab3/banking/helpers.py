BankStorage = dict()
from uuid import UUID


def get_all_banks():
    return BankStorage.values()


def get_account(account_id):
    if not isinstance(account_id, str) and not isinstance(account_id, UUID):
        return account_id

    for bank in BankStorage.values():
        account = bank.get_account(account_id)
        if account is not None:
            return account

    return None