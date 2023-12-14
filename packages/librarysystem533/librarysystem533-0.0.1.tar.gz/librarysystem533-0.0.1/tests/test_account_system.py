import unittest
from unittest.mock import patch, mock_open
from user.account_system import AccountSystem
import io

# Test data for books and users in CSV format
book_csv_data = 'book_id,title,author,published_year,ISBN,is_available,First_entry_date,times_borrowed,borrowed_user,last_borrow_date,last_return_date\n1,One Day,David Nicholls,2009,978-0274808465,yes,2023/1/1,4,,2023-12-11,2023-12-04,2023-12-11\n'
user_csv_data = 'account_name,password,first_name,last_name,birthdate,email,phone,address,borrowed_book,permission\nmimi,12345,mimi,Lin,1988-09-12,mimilin@hotmail.com,0912345678,Vancouver,NA,normal\n'

class TestAccountSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up class-wide attributes
        cls.user_name = 'mimi'

    @classmethod
    def tearDownClass(cls):
        # Clean up class-wide attributes after all tests are done
        del cls.user_name

    def setUp(self):
        # Set up before each test method
        self.account_system = AccountSystem()

    def tearDown(self):
        # Teardown method for each test method
        del self.account_system

    def mock_open_helper(self, path, *args, **kwargs):
        """Helper function to return different mock data based on file path."""
        if path == 'Librarysystem/database/book.csv':
            return mock_open(read_data=book_csv_data).return_value
        elif path == 'Librarysystem/database/user.csv':
            return mock_open(read_data=user_csv_data).return_value
        else:
            return mock_open().return_value

    @patch('builtins.input', side_effect=['account', 'password', 'John', 'Doe', '2000-01-01', 'john@example.com', '1234567890', '123 Main St'])
    @patch('builtins.open', new_callable=mock_open)
    def test_create_account(self, mock_file, mock_input):
        mock_file.side_effect = self.mock_open_helper
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.account_system.create_account()
            self.assertIn('Account created successfully.', mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['1', 'john@example.com'])
    @patch('builtins.open', new_callable=mock_open)
    def test_update_profile(self, mock_file, mock_input):
        mock_file.side_effect = self.mock_open_helper
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.account_system.update_profile(self.user_name)
            self.assertIn('Profile updated successfully.', mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['password', 'password'])
    @patch('builtins.open', new_callable=mock_open)
    def test_reset_password(self, mock_file, mock_input):
        mock_file.side_effect = self.mock_open_helper
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.account_system.reset_password(self.user_name)
            self.assertIn('Password has been reset successfully.', mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
