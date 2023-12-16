import datetime
import uuid 

class Account:
    def __init__(self, account_number, initial_balance,password):
        self.account_id = account_number
        self.balance = initial_balance
        self.transaction_history = []
        self.password = password 

    def add_transaction(self, amount, transaction_type):
        date = datetime.datetime.now().date().strftime('%Y-%m-%d') 
        trans_id = str(uuid.uuid4())
        transaction = {
            'Date': date,
            'Amount': amount,
            'Type': transaction_type,
            'Transaction Id': trans_id,
            "Account Id":self.account_id 
        }
        self.transaction_history.append(transaction)
        self.update_balance(amount, transaction_type)
    def update_balance(self, amount, transaction_type):
        if transaction_type == 'deposit':
            self.balance = self.balance + amount
        elif transaction_type == 'withdrawal':
            self.balance -= amount
        elif transaction_type == 'transfer':
            self.balance += amount

class AccountControl:
    def __init__(self):
        self.account = {}
    def add_account(self, account):
        self.account[account.account_id] = account
            
    def check_balance(self, account_id): 
        try:
            return self.account[account_id].balance
        except KeyError:
            print("Account not found.")    
    def print_transaction_history(self, transactions):
        for i in transactions:
            print(f"Date: {i['Date']}, "
                  f"Amount: {i['Amount']}, "
                  f"Type: {i['Type']}, "
                  f"Transaction Id: {i['Transaction Id']}, "
                  f"Account Id: {i['Account Id']}")


    def view_transaction_history(self, start_date=None, end_date=None):
        temp = []
        if isinstance(start_date, str):
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
        if isinstance(end_date, str):
                end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date and end_date:
                    for account_id in self.account:
                        account = self.account[account_id]
                        for transaction in account.transaction_history:
                            transaction_date = datetime.datetime.strptime(transaction['Date'], '%Y-%m-%d').date()
                            if start_date <= transaction_date and transaction_date <= end_date:
                                temp.append(transaction)
        else:
            u_input = input("Please enter a time range or type 'all' to view whole history: ")
            if u_input.lower() == 'all':
                temp = self.account.transaction_history
            else:
                try:
                    transdate = datetime.datetime.strptime(u_input, '%Y-%m-%d').date()
                    date = transdate.strftime('%Y-%m-%d')
                    for i in self.account.transaction_history:
                        if i['Date'] == date:
                            temp.append(i)
                    if not temp:
                        print(f"No transactions on this date: {date}")
                         

                except ValueError:
                    print(" Please use 'YYYY-MM-DD' format.")
        
        self.print_transaction_history(temp)    
        return temp 
    def execute_transaction(self, account_id, amount, transaction_type):
        if account_id in self.account:
            account = self.account[account_id]
            if transaction_type == 'deposit' or transaction_type =='withdrawal' or transaction_type == 'transfer':
                account.add_transaction(amount, transaction_type)
            else:
                raise ValueError("Invalid transaction type")
        else:
            raise KeyError("Account ID not found")
