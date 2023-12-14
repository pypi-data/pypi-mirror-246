import unittest
from unittest.mock import patch, mock_open
from user.user_action import UserAction
import io

# Test data for user in CSV format
user_csv_data = 'account_name,password,first_name,last_name,birthdate,email,phone,address,borrowed_book,permission\nmimi,12345,mimi,Lin,1988-09-12,mimilin@hotmail.com,12345566,Vancouver,NA,normal\n'

class TestUserAction(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up class-level attribute, executed once before all tests
        cls.user_name = 'mimi'

    @classmethod
    def tearDownClass(cls):
        # Clean up class-level attribute, executed once after all tests
        del cls.user_name

    def setUp(self):
        # Set up before each test method
        self.user_action = UserAction()

    def tearDown(self):
        # Clean up after each test method
        del self.user_action

    @patch('builtins.input', side_effect=['3'])
    def test_start_exit(self, mock_input):
        # Test the exit functionality of the start method
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout, self.assertRaises(SystemExit):
            self.user_action.start()
            self.assertIn('See you next time.', mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['4', '3'])
    def test_start_error(self, mock_input):
        # Test handling of invalid input in the start method
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout, self.assertRaises(SystemExit):
            self.user_action.start()
            self.assertIn("Error: Invalid input", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['1', 'mimi', '1245', '1', 'mimi', '12345', '7', '3'])
    @patch('builtins.open', new_callable=mock_open, read_data=user_csv_data)
    @patch.object(UserAction, 'main_app')
    def test_start_login(self, mock_main_app, mock_file, mock_input):
        # Test login functionality and transition to main app
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout, self.assertRaises(SystemExit):
            self.user_action.start()
            self.assertIn('Invalid', mock_stdout.getvalue())
            self.assertIn('account name', mock_stdout.getvalue())
            self.assertIn('or password.', mock_stdout.getvalue())
        mock_main_app.assert_called_once()

    @patch('builtins.input', side_effect=['7'])
    def test_main_app_log_out(self, mock_input):
        # Test log out functionality from main app
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.user_action.user = self.user_name
            self.user_action.main_app()
            self.assertIn(f'Account:\t{self.user_name}', mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
