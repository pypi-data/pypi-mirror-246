import unittest
from unittest.mock import patch
from pack2module2 import CustomerService 

class TestCustomerService(unittest.TestCase):

    def setUp(self):
        self.customer_service = CustomerService()

    def tearDown(self):
        del self.customer_service

    @patch('builtins.input', side_effect=['This is a test message.'])
    def test_save_message(self, mock_input):
        self.customer_service.save_message()
        self.assertIn('This is a test message.', self.customer_service.messages_storage)
        self.assertEqual(len(self.customer_service.messages_storage), 1)
        self.assertIsInstance(self.customer_service.messages_storage, list)
        self.assertEqual(self.customer_service.messages_storage[0], 'This is a test message.')

    @patch('builtins.input', side_effect=['email', 'contact_NO', 'invalid', 'email'])
    def test_customer_service_responses(self, mock_input):
        # Testing for 'email' response
        self.customer_service.customer_service()
        self.assertEqual(mock_input.call_args_list[0][0][0], """Please choose the following options: 'email' if you would like to learn about our app functions" 
                               or 'contact_NO' if you would like to contact our human serive""")
        # Testing for 'contact_NO' response
        self.customer_service.customer_service()
        self.assertEqual(mock_input.call_args_list[1][0][0],  """Please choose the following options: 'email' if you would like to learn about our app functions" 
                               or 'contact_NO' if you would like to contact our human serive""")
        # Testing for invalid response
        self.customer_service.customer_service()
        self.assertEqual(mock_input.call_args_list[2][0][0],  """Please choose the following options: 'email' if you would like to learn about our app functions" 
                               or 'contact_NO' if you would like to contact our human serive""")
        # Testing for another 'email' response
        self.customer_service.customer_service()
        self.assertEqual(mock_input.call_args_list[3][0][0],  """Please choose the following options: 'email' if you would like to learn about our app functions" 
                               or 'contact_NO' if you would like to contact our human serive""")
    def test_calculate_loan_repayment(self):
        loan_repayment = self.customer_service.calculate_loan_repayment(10000, 60)
        self.assertEqual(loan_repayment['monthly_repayment'], 188.71)
        self.assertEqual(loan_repayment['total_repayment'], 11322.6)
        self.assertIsInstance(loan_repayment, dict)
        self.assertGreater(loan_repayment['total_repayment'], loan_repayment['monthly_repayment'])

if __name__ == '__main__':
    unittest.main()