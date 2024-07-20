from users import User
import json
import os

class ATM:
    def __init__(self, data_file="users.json"):
        self.data_file = data_file
        self.users = self.load_users()

    def load_users(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                data = json.load(file)
                return {account: User.from_dict(info) for account, info in data.items()}
        else:
            return {}

    def save_users(self):
        with open(self.data_file, "w") as file:
            json.dump({account: user.to_dict() for account, user in self.users.items()}, file, indent=4)

    def add_user(self, account_number, pin, password, email, balance=0):
        if account_number in self.users:
            raise ValueError("Account already exists")
        self.users[account_number] = User(account_number, pin, password, email, balance)
        self.save_users()

    def authenticate_user(self, account_number, pin):
        user = self.users.get(account_number)
        if user and user.pin == pin:
            return user
        return None

    def authenticate_email_password(self, email, password):
        for user in self.users.values():
            if user.email == email and user.password == password:
                return user
        return None

    def reset_pin(self, email, password, new_pin):
        user = self.authenticate_email_password(email, password)
        if user:
            user.pin = new_pin
            self.save_users()
            return True
        return False

    def run(self):
        while True:
            print("\nWelcome to the ATM")
            print("1. Create Account")
            print("2. Login")
            print("3. Reset PIN")
            print("4. Exit")
            choice = input("Choose an option: ")

            if choice == '1':
                self.create_account()
            elif choice == '2':
                self.login()
            elif choice == '3':
                self.reset_pin_option()
            elif choice == '4':
                break
            else:
                print("Invalid option. Please try again.")

    def create_account(self):
        account_number = input("Enter a new account number: ")
        pin = input("Enter a new PIN: ")
        password = input("Enter a new password: ")
        email = input("Enter your email: ")
        try:
            self.add_user(account_number, pin, password, email)
            print("Account created successfully.")
        except ValueError as e:
            print(e)

    def login(self):
        account_number = input("Enter your account number: ")
        pin = input("Enter your PIN: ")
        user = self.authenticate_user(account_number, pin)
        if user:
            self.user_menu(user)
        else:
            print("Authentication failed. Please try again.")

    def reset_pin_option(self):
        email = input("Enter your email: ")
        password = input("Enter your password: ")
        new_pin = input("Enter a new PIN: ")
        if self.reset_pin(email, password, new_pin):
            print("PIN reset successfully.")
        else:
            print("Invalid email or password. PIN reset failed.")

    def user_menu(self, user):
        while True:
            print("\nATM Menu:")
            print("1. Check Balance")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. View Transaction History")
            print("5. Logout")
            choice = input("Choose an option: ")

            if choice == '1':
                print(f"Your balance is ${user.check_balance()}")
            elif choice == '2':
                amount = float(input("Enter amount to deposit: "))
                user.deposit(amount)
                self.save_users()
                print(f"${amount} deposited successfully.")
            elif choice == '3':
                amount = float(input("Enter amount to withdraw: "))
                try:
                    user.withdraw(amount)
                    self.save_users()
                    print(f"${amount} withdrawn successfully.")
                except ValueError as e:
                    print(e)
            elif choice == '4':
                print("\nTransaction History:")
                for transaction in user.transaction_history:
                    print(transaction)
            elif choice == '5':
                break
            else:
                print("Invalid option. Please try again.")

# Initialize and run the ATM
atm = ATM()
atm.run()
