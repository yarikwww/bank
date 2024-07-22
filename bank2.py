
import unittest
from unittest.mock import patch
class Account:
    def __init__(self, balance, account_number):
        self._balance = balance
        self._account_number = account_number

    @classmethod
    def create_account(cls, account_number):
        return cls(0.0, account_number)

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
        else:
            raise ValueError('Amount must be positive')

    def withdraw(self, amount):
        if amount > 0:
            self._balance -= amount
        else:
            raise ValueError('Amount must be positive')

    def get_balance(self):
        return self._balance

    def get_account_number(self):
        return self._account_number

    def __str__(self):
        return f'Account number: {self._account_number}, balance: {self._balance}'


class SavingsAccount(Account):
    def __init__(self, balance, account_number, interest_rate):
        super().__init__(balance, account_number)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self._balance * self.interest_rate / 100
        self._balance += interest

    def __str__(self):
        return f'Savings Account number: {self._account_number}, balance: {self._balance}, interest rate: {self.interest_rate}%'


class CurrentAccount(Account):
    def __init__(self, balance, account_number, overdraft_limit):
        super().__init__(balance, account_number)
        self.overdraft_limit = overdraft_limit

    def is_overdraft(self):
        return self._balance < 0

    def __str__(self):
        return f'Current Account number: {self._account_number}, balance: {self._balance}, overdraft limit: {self.overdraft_limit}'


class Bank:
    def __init__(self):
        self.accounts = []

    def open_account(self, account):
        self.accounts.append(account)

    def close_account(self, account_number):
        self.accounts = [account for account in self.accounts if account.get_account_number() != account_number]

    def pay_dividend(self, amount):
        for account in self.accounts:
            account.deposit(amount)

    def update(self):
        for account in self.accounts:
            if isinstance(account, SavingsAccount):
                account.add_interest()
            elif isinstance(account, CurrentAccount):
                if account.is_overdraft():
                    print(f'Account number {account.get_account_number()} is in overdraft. Please take action.')

    def __str__(self):
        return '\n'.join(str(account) for account in self.accounts)



if __name__ == "__main__":
    bank = Bank()

    # Creating accounts
    sa1 = SavingsAccount(1000, 'SA123', 5)
    sa2 = SavingsAccount(2000, 'SA124', 4)
    ca1 = CurrentAccount(500, 'CA123', 1000)
    ca2 = CurrentAccount(-200, 'CA124', 500)


    bank.open_account(sa1)
    bank.open_account(sa2)
    bank.open_account(ca1)
    bank.open_account(ca2)

    print("Initial state of accounts:")
    print(bank)


    bank.update()

    print("\nState of accounts after update:")
    print(bank)


    bank.pay_dividend(50)

    print("\nState of accounts after paying dividend:")
    print(bank)

    # Closing an account
    bank.close_account('SA123')

    print("\nState of accounts after closing an account:")
    print(bank)


class TestBank(unittest.TestCase):

    def test_update(self):
        bank = Bank()

        # Create test accounts
        sa1 = SavingsAccount(1000, 'SA126', 5)
        sa2 = SavingsAccount(2000, 'SA127', 4)
        ca1 = CurrentAccount(500, 'CA126', 1000)
        ca2 = CurrentAccount(-200, 'CA127', 500)


        bank.open_account(sa1)
        bank.open_account(sa2)
        bank.open_account(ca1)
        bank.open_account(ca2)


        with patch('builtins.print') as mocked_print:

            bank.update()


            self.assertEqual(sa1.get_balance(), 1050)  # 5% interest on 1000
            self.assertEqual(sa2.get_balance(), 2080)  # 4% interest on 2000


            mocked_print.assert_called_with('Account number CA127 is in overdraft. Please take action.')


if __name__ == "__main__":
    unittest.main()
