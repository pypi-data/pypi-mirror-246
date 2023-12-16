import unittest
from module2 import FinancialServices 
from module1 import Account, AccountControl

class TestFinancialServices(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up TestFinancialServices class...")
        cls.financial_services = FinancialServices()
        cls.account1 = Account("123456", 1000, "password123")
        cls.account2 = Account("654321", 2000, "password321")
        cls.financial_services.account_control.add_account(cls.account1)
        cls.financial_services.account_control.add_account(cls.account2)

    @classmethod
    def tearDownClass(cls):
        del cls.account1
        del cls.account2  
        del cls.financial_services
        
        print("Tearing down TestFinancialServices class...")

    def setUp(self):
        self.financial_services.account_control.account["123456"].balance = 1000
        self.financial_services.account_control.account["654321"].balance = 2000

    def tearDown(self):
        self.financial_services.account_control.account["123456"].balance = 1000
        self.financial_services.account_control.account["654321"].balance = 2000
        self.financial_services.account_control.account["123456"].transaction_history.clear()
        self.financial_services.account_control.account["654321"].transaction_history.clear()        

    def test_fund_transfer(self):
        print("Initial Balance of 123456:", self.financial_services.account_control.account["123456"].balance)
        print("Initial Balance of 654321:", self.financial_services.account_control.account["654321"].balance)
    
        result = self.financial_services.fund_transfer("123456", "654321", 500)
    
        print("Balance of 123456 after transfer:", self.financial_services.account_control.account["123456"].balance)
        print("Balance of 654321 after transfer:", self.financial_services.account_control.account["654321"].balance)

        self.assertEqual(result, "Fund transfer successful.")
        self.assertEqual(self.financial_services.account_control.account["123456"].balance, 500)
        self.assertEqual(self.financial_services.account_control.account["654321"].balance, 2500)
        total_balance = self.financial_services.account_control.account["123456"].balance + self.financial_services.account_control.account["654321"].balance
        self.assertEqual(total_balance, 3000)        
         
    def test_deposit_and_withdrawal(self):
            print("Initial Balance:", self.financial_services.account_control.account["123456"].balance)
            
            self.financial_services.deposit("123456", 300)
            self.financial_services.deposit("123456", -300) 
            balance_after_deposit = self.financial_services.account_control.account["123456"].balance
            print("Balance after deposit:", balance_after_deposit)
        
            self.financial_services.withdrawal("123456", 500)
            balance_after_withdrawal = self.financial_services.account_control.account["123456"].balance
            print("Balance after withdrawal:", balance_after_withdrawal)
        
            self.assertEqual(balance_after_deposit, 1300)
            self.assertEqual(balance_after_withdrawal, 800)  
            self.assertEqual(balance_after_deposit - 1000, 300)
            self.assertEqual(1300 - balance_after_withdrawal, 500)    
if __name__ == '__main__':
    unittest.main()
