import mysql.connector
from mysql.connector import errorcode
from decimal import Decimal

class Database:
    def __init__(self):
        try:
            self.con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="1234",
                database="bank",
                auth_plugin='mysql_native_password'
            )
            print('Database connected')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
            exit(1)

        self.create_table()

    def create_table(self):
        query = """
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(255) UNIQUE,
                password VARCHAR(255),
                balance DECIMAL(10, 2) DEFAULT 0
            )
        """
        cur = self.con.cursor()
        cur.execute(query)
        self.con.commit()

    def save_user(self, username, password):
        try:
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cur = self.con.cursor()
            cur.execute(query, (username, password))
            self.con.commit()
            print('User saved to Database')
        except mysql.connector.IntegrityError:
            print("Username already exists. Please choose a different username.")
        except Exception as e:
            print("An Error has occurred ", str(e))

    def fetch_all(self):
        query = "SELECT * FROM users"
        cur = self.con.cursor()
        cur.execute(query)
        for row in cur:
            print(row)

    def fetch_one(self, username):
        query = "SELECT * FROM users WHERE username = %s"
        cur = self.con.cursor()
        cur.execute(query, (username,))
        for row in cur:
            print(row)

    def delete_user(self, username):
        try:
            query = "DELETE FROM users WHERE username = %s"
            cur = self.con.cursor()
            cur.execute(query, (username,))
            self.con.commit()
            print("User deleted successfully")
        except Exception as e:
            print("Some Error occurred ", str(e))

    def change_username(self, username, new_name):
        query = "UPDATE users SET username = %s WHERE username = %s"
        cur = self.con.cursor()
        cur.execute(query, (new_name, username))
        self.con.commit()
        print("Username changed successfully")

    def change_password(self, username, new_password):
        query = "UPDATE users SET password = %s WHERE username = %s"
        cur = self.con.cursor()
        cur.execute(query, (new_password, username))
        self.con.commit()
        print("Password changed successfully")

    def login_user(self, username, password):
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cur = self.con.cursor()
        cur.execute(query, (username, password))
        user_data = cur.fetchone()
        if user_data:
            print("Login successful!")
            return user_data
        else:
            print("Invalid Login credentials")
            return None

    def update_balance(self, amount, username):
        query = "UPDATE users SET balance = %s WHERE username = %s"
        cur = self.con.cursor()
        cur.execute(query, (amount, username))
        self.con.commit()

    def fetch_balance(self, username):
        query = "SELECT balance FROM users WHERE username = %s"
        cur = self.con.cursor()
        cur.execute(query, (username,))
        result = cur.fetchone()
        if result:
            return result[0]
        else:
            return None

class BankAccount:
    def __init__(self, account_number, username, password, initial_balance=0.0):
        self.account_number = account_number
        self.username = username
        self.password = password
        self.balance = initial_balance

    def deposit(self, amount):
        amount = Decimal(str(amount)) 
        self.balance += amount
        db.update_balance(self.balance, self.username)
        print(f"Deposited {amount} into account number {self.account_number}.")
        print(f"Current balance: {self.balance}")

    def withdraw(self, amount):
        amount = Decimal(str(amount))
        if self.balance >= amount:
            self.balance -= amount
            db.update_balance(self.balance, self.username)
            print(f"Withdrew {amount} from account number {self.account_number}.")
            print(f"Current balance: {self.balance}")
        else:
            print("Insufficient balance.")

    def get_balance(self):
        print(f"Account number: {self.account_number}")
        print(f"Username: {self.username}")
        print(f"Current balance: {self.balance}")

def create_account():
    print("Account Creation")
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    db.save_user(username, password)

    user_data = db.login_user(username, password)
    if user_data:
        account_number = user_data[0]
        balance = user_data[3]
        print(f"Account created successfully! \n Account number: {account_number}")
        return BankAccount(account_number, username, password, balance)
    else:
        return None

def login():
    print("Login")
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    user_data = db.login_user(username, password)
    if user_data:
        account_number, _, _, balance = user_data
        print(f"Welcome, {username}!")
        return BankAccount(account_number, username, password, balance)
    else:
        return None

def main():
    print("************Welcome to the Our_Bank*****************")

    while True:
        print("\nPlease select an option:")
        print("1. Login")
        print("2. Create an account")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            account = login()
            if account is not None:
                banking_operations(account)
        elif choice == "2":
            account = create_account()
            if account is not None:
                banking_operations(account)
        elif choice == "3":
            print("Thank you for using the banking application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def banking_operations(account):
    while True:
        print("\nPlease select an option:")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Logout")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            amount = float(input("Enter amount to deposit: "))
            account.deposit(amount)
        elif choice == "2":
            amount = float(input("Enter amount to withdraw: "))
            account.withdraw(amount)
        elif choice == "3":
            account.get_balance()
        elif choice == "4":
            print("Logged out.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    db = Database()
    main()