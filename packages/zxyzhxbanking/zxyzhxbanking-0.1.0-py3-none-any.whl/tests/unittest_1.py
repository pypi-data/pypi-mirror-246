import unittest
from module1 import Account, AccountControl  
from pack2module1 import Authorize 

class MockAccountControl:
    def __init__(self):
        self.accounts = {}
        self.account = {}
    def add_account(self, account):
        self.accounts[account.account_number] = account
        self.account[account.account_number] = account
class TestAuthorize(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up class resources for TestAuthorize")
        cls.mock_account_control = MockAccountControl()

    @classmethod
    def tearDownClass(cls):
        print("Tearing down class resources for TestAuthorize")
        del cls.mock_account_control

    def setUp(self):
        self.authorize = Authorize('123456', 'password123', self.mock_account_control)
        self.authorize.add_user('user1', 'pass1')
        self.authorize.add_user('user2', 'pass2')

    def tearDown(self):
        del self.authorize

    def test_add_user(self):
        self.assertIn('user1', self.authorize.accounts)
        self.assertIn('user2', self.authorize.accounts)
        self.assertNotIn('user3', self.authorize.accounts)
        self.assertEqual(self.authorize.accounts['user1'], 'pass1')

    def test_login_logout(self):
        self.assertTrue(self.authorize.login('user1', 'pass1'))
        self.assertEqual(self.authorize.current_user, 'user1')
        self.authorize.logout()
        self.assertIsNone(self.authorize.current_user)
        self.assertFalse(self.authorize.login('user1', 'wrongpass'))

    def test_delete_account(self):
    # Ensure user2 exists before deletion
        self.assertIn('user2', self.authorize.accounts)
        self.assertIn('user2', self.mock_account_control.account)

    # Perform the deletion
        self.authorize.delete_account('user2')

    # Check if user2 is removed from authorize.accounts
        self.assertNotIn('user2', self.authorize.accounts)

    # Check if user2 is removed from mock_account_control.account
        self.assertNotIn('user2', self.mock_account_control.account)

    # Ensure user1 still exists
        self.assertIn('user1', self.authorize.accounts)
        self.assertIn('user1', self.mock_account_control.account)

    # Attempt to delete a non-existing user and check nothing changes
        original_account_count = len(self.authorize.accounts)
        self.authorize.delete_account('nonexistent_user')
        self.assertEqual(len(self.authorize.accounts), original_account_count)
        self.assertNotIn('nonexistent_user', self.authorize.accounts)

    def test_check_login_status(self):
        self.authorize.login('user1', 'pass1')
        self.assertEqual(self.authorize.current_user, 'user1')
        self.authorize.logout()
        self.assertIsNone(self.authorize.current_user)

if __name__ == '__main__':
    unittest.main()