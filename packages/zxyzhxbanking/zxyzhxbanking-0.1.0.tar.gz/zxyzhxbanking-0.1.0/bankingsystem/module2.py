from module1 import AccountControl
class FinancialServices:
    def __init__(self):
        self.account_control = AccountControl()

    def fund_transfer(self, first_account_id, sec_account_id, amount):
        balance = self.account_control.check_balance(first_account_id)
        if balance >= amount:
            self.account_control.execute_transaction(first_account_id, -amount, 'transfer')
            self.account_control.execute_transaction(sec_account_id, amount, 'transfer')
            return "Fund transfer successful."
        else:
            return "Insufficient balance to transfer."

    def deposit(self, user_id, amount):
        try:
            if amount <= 0:
                raise ValueError("Deposit amount must be positive.")
            self.account_control.execute_transaction(user_id, amount, 'deposit')
            return "Deposit successful."
        except ValueError as e:
            return str(e)
        except Exception as e:
            return f"An error occurred: {e}"

    def withdrawal(self, user_id, amount):
        available_balance = self.account_control.check_balance(user_id)
        if available_balance >= amount:
            self.account_control.execute_transaction(user_id, amount, 'withdrawal')
            return "Withdrawal successful."
        else:
            return "Insufficient balance to withdrawal."
