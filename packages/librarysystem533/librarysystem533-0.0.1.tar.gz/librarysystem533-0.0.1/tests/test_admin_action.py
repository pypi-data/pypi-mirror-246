import unittest
from unittest.mock import patch, mock_open
from admin.admin_action import AdminAction, UserManagementError, BookManagementError
import io

# Test data for admins in CSV format
admin_csv_data = 'admin_id,user_name,password,title\n1,jamie,jamie1,staff\n2,erin,erin1,manager\n'

class TestAdminAction(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        # Set up class-wide attributes
        cls.title = 'staff'

    @classmethod
    def tearDownClass(cls):
        # Clean up class-wide attributes after all tests are done
        del cls.title

    def setUp(self):
        # Set up before each test method
        self.action = AdminAction()

    def tearDown(self):
        # Teardown method for each test method
        del self.action

    @patch('builtins.input', side_effect=['jamie', 'jamie1'])
    @patch('builtins.open', new_callable=mock_open, read_data=admin_csv_data)
    def test_login_admin_success(self, mock_file, mock_input):
        # Test successful admin login
        title = self.action.login_admin()
        self.assertTrue(self.action.logged_in)
        self.assertEqual(title, self.title)

    @patch('builtins.input', side_effect=['user', 'wrong_password'])
    @patch('builtins.open', new_callable=mock_open, read_data=admin_csv_data)
    def test_login_admin_failure(self, mock_file, mock_input):
        # Test failed admin login
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            title = self.action.login_admin()
            self.assertFalse(self.action.logged_in)
            self.assertIn('Invalid username or password.', mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['3'])
    @patch.object(AdminAction, 'user_management_interface')
    @patch.object(AdminAction, 'book_management_interface')
    def test_main_interface(self, mock_book_interface, mock_user_interface, mock_input):
        # Test main interface functionality
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.action.main_interface()
            mock_user_interface.assert_not_called()
            mock_book_interface.assert_not_called()
            self.assertIn('Logging out...', mock_stdout.getvalue())
            self.assertFalse(self.action.logged_in)

    @patch('builtins.input', side_effect=['1', '3'])  
    @patch.object(AdminAction, 'user_management_interface')
    @patch.object(AdminAction, 'book_management_interface')
    def test_user_management_interface(self, mock_book_interface, mock_user_interface, mock_input):
        # Test user management interface within main interface
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.action.main_interface()
            self.assertIn('1: User Management', mock_stdout.getvalue())
            self.assertIn('2: Book Management', mock_stdout.getvalue())
            self.assertIn('3: Logout', mock_stdout.getvalue())
            mock_user_interface.assert_called_once()
            mock_book_interface.assert_not_called()
            self.assertIn('Logging out...', mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['2', '3'])  
    @patch.object(AdminAction, 'user_management_interface')
    @patch.object(AdminAction, 'book_management_interface')
    def test_book_management_interface(self, mock_book_interface, mock_user_interface, mock_input):
        # Test book management interface
        self.action.main_interface()
        mock_book_interface.assert_called_once()
        mock_user_interface.assert_not_called()

    @patch('builtins.input', side_effect=['jamie', 'jamie1', '3'])
    @patch('builtins.open', new_callable=mock_open, read_data=admin_csv_data)
    @patch.object(AdminAction, 'main_interface')
    def test_start(self, mock_main_interface, mock_file, mock_input):
        # Test the start method of AdminAction
        self.action.start()
        mock_main_interface.assert_called_once()

    '''
    Following is error tests
    '''
    @patch('builtins.input', side_effect=['jamie', 'jamie1'])
    @patch('builtins.open', side_effect=FileNotFoundError())
    def test_login_admin_file_not_found(self, mock_file, mock_input):
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            title = self.action.login_admin()
            self.assertIn("Error: File", mock_stdout.getvalue())
            self.assertIsNone(title)

    @patch('builtins.input', side_effect=['1'])
    @patch('admin.user_management_system.UserManagementSystem.user_interface', side_effect=Exception('Test Exception'))
    def test_user_management_interface_exception(self, mock_user_interface, mock_input):
        with self.assertRaises(UserManagementError):
            self.action.user_management_interface()

    @patch('builtins.input', side_effect=['2'])
    @patch('admin.book_management_system.BookManagementSystem.book_interface', side_effect=Exception('Test Exception'))
    def test_book_management_interface_exception(self, mock_book_interface, mock_input):
        with self.assertRaises(BookManagementError):
            self.action.book_management_interface()

if __name__ == '__main__':
    unittest.main()
