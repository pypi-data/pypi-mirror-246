from module1 import Account, AccountControl
class Authorize(Account):
    def __init__(self, account_number, password, account_control):
        super().__init__(account_number, 0, password)
        self.accounts = {}  
        self.current_user = None
        self.account_control = account_control 

    def add_user(self, username, password):
        if username not in self.accounts:
            self.accounts[username] = password
            print(f"User {username} added successfully.")
        else:
            print("User already exists.")

    def login(self, entered_account_number, entered_password):
        if entered_account_number in self.accounts and self.accounts[entered_account_number] == entered_password:
            self.current_user = entered_account_number
            print(f"Login successful, welcome {entered_account_number}!")
            return True
        else:
            print("Login failed, incorrect account number or password.")
            return False

    def logout(self):
        if self.current_user:
            print(f"User {self.current_user} has logged out.")
            self.current_user = None
        else:
            print("No user is currently logged in.")

    def delete_account(self, username):
        if username in self.accounts:
            account = self.account_control.account.get(username)
            if account and account.balance == 0:
                del self.accounts[username]
                del self.account_control.account[username]
                print(f"Account {username} has been deleted.")
            else:
                print(f"Account {username} cannot be deleted due to non-zero balance or not existing.")
        else:
            print(f"Account {username} does not exist, deletion failed.")

    def check_login_status(self):
        if self.current_user:
            print(f"Currently logged in user: {self.current_user}")
        else:
            print("Currently in not logged in status.")