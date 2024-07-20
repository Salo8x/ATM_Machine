import json
import os

class User:
    def __init__(self, account_number, pin, password, email, balance=0):
        self.account_number = account_number
        self.pin = pin
        self.password = password
        self.email = email
        self.balance = balance
        self.transaction_history = []

    def check_balance(self):
        return self.balance

    def deposit(self, amount):
        self.balance += amount
        self.transaction_history.append(f"Deposited: ${amount}")
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.transaction_history.append(f"Withdrew: ${amount}")
        return self.balance

    def to_dict(self):
        return {
            'account_number': self.account_number,
            'pin': self.pin,
            'password': self.password,
            'email': self.email,
            'balance': self.balance,
            'transaction_history': self.transaction_history
        }

    @staticmethod
    def from_dict(data):
        user = User(data['account_number'], data['pin'], data['password'], data['email'], data['balance'])
        user.transaction_history = data['transaction_history']
        return user
