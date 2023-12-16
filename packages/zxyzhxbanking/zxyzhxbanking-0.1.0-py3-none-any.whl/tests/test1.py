import datetime
import unittest
from module1 import AccountControl, Account

class TestAccountControl(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.account1 = Account("123456", 1000, "password123")
        cls.account2 = Account("654321", 500, "password321")
        print("Setting up TestAccountControl class...")

    @classmethod
    def tearDownClass(cls):
        del cls.account1
        del cls.account2
        print("Tearing down TestAccountControl class...")

    def setUp(self):
        self.account_control = AccountControl()
        self.account_control.add_account(self.account1)
        self.account_control.add_account(self.account2)

    def tearDown(self):
        del self.account_control

    def test_check_and_execute_balance(self):
        balance1 = self.account_control.check_balance("123456")
        self.assertEqual(balance1, 1000)
        self.account_control.execute_transaction("123456", 200, "deposit")
        balance2 = self.account_control.check_balance("123456")
        self.assertEqual(balance2, 1200)
        self.account_control.execute_transaction("123456", 100, "withdrawal")
        balance3 = self.account_control.check_balance("123456")
        self.assertEqual(balance3, 1100)
        self.assertNotEqual(balance1, balance3)

    def test_invalid_account_operations(self):
        self.assertIsNone(self.account_control.check_balance("000000"))
        with self.assertRaises(ValueError):
            self.account_control.execute_transaction("123456", 200, "invalid_type")
        with self.assertRaises(KeyError):
            self.account_control.execute_transaction("000000", 100, "deposit")
        self.assertNotIn("000000", self.account_control.account)
    def test_view_transaction_history(self):

        self.account1.add_transaction(100, 'deposit')
        self.account1.add_transaction(50, 'withdrawal')
    
    
        start_date = datetime.date(2023, 1, 1)
        end_date = datetime.date(2023, 12, 31)
        transactions = self.account_control.view_transaction_history(start_date, end_date)
        print("Transactions:", transactions)
       
        self.assertIsInstance(transactions, list)
        is_amount_100_present = any(transaction['Amount'] == 100 for transaction in transactions)
        is_amount_1000_present = any(transaction['Amount'] == 1000 for transaction in transactions) 
        self.assertTrue(is_amount_100_present)
        self.assertFalse(is_amount_1000_present)
    
    
if __name__ == '__main__':
    unittest.main()
