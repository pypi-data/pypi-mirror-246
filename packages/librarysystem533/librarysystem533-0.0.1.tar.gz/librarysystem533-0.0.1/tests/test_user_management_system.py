import unittest
from unittest.mock import patch, mock_open
from admin.user_management_system import UserManagementSystem
import io

# Test data for users in CSV format
user_csv_data = 'account_name,password,first_name,last_name,birthdate,email,phone,address,borrowed_book,permission\nmimi,12345,mimi,Lin,1988-09-12,mimilin@hotmail.com,12345566,Vancouver,NA,normal\n'

class TestUserManagementSystem(unittest.TestCase):

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
        self.user_system = UserManagementSystem()

    def tearDown(self):
        # Clean up after each test method
        del self.user_system

    @patch('builtins.input', return_value='mimi')
    @patch('builtins.open', new_callable=mock_open, read_data=user_csv_data)
    def test_delete_user_success(self, mock_file, mock_input):
        # Test deleting an existing user successfully
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.user_system.delete_user()
            self.assertIn("User 'mimi' has been deleted.", mock_stdout.getvalue())

    @patch('builtins.input', return_value='kitty')
    @patch('builtins.open', new_callable=mock_open, read_data=user_csv_data)
    def test_delete_user_failure(self, mock_file, mock_input):
        # Test deleting a non-existing user
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.user_system.delete_user()
            self.assertIn("No user found with the account name 'kitty'.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['mimi', 'prohibit'])
    @patch('builtins.open', new_callable=mock_open, read_data=user_csv_data)
    def test_update_permissions_success(self, mock_file, mock_input):
        # Test updating permissions of a user successfully
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.user_system.update_permissions()
            self.assertIn("Permissions updated for user 'mimi'.", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['mimi', 'abab'])
    @patch('builtins.open', new_callable=mock_open, read_data=user_csv_data)
    def test_update_permissions_failure(self, mock_file, mock_input):
        # Test updating permissions with an invalid permission level
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.user_system.update_permissions()
            self.assertIn("Invalid permission level.", mock_stdout.getvalue())

    @patch('builtins.input', return_value='mimi')
    @patch('builtins.open', new_callable=mock_open, read_data=user_csv_data)
    def test_user_details_existing_user(self, mock_file, mock_input):
        # Test retrieving details of an existing user
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.user_system.user_details()
            self.assertIn("User Details:", mock_stdout.getvalue())
            self.assertIn(f"account_name: {self.user_name}", mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['5'])
    def test_user_interface(self, mock_input):
        # Test the user interface, specifically the exit functionality
        with self.assertRaises(SystemExit):
            self.user_system.user_interface()

if __name__ == '__main__':
    unittest.main()
