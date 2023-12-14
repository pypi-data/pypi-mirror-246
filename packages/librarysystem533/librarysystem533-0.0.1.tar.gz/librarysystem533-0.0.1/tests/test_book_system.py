import unittest
from unittest.mock import patch, mock_open
from user.book_system import BookSystem
import io

# Test data for books and users in CSV format
book_csv_data = 'book_id,title,author,published_year,ISBN,is_available,First_entry_date,times_borrowed,borrowed_user,last_borrow_date,last_return_date\n1,One Day,David Nicholls,2009,978-0274808465,yes,2023/1/1,4,,2023-12-11,2023-12-04,2023-12-11\n'
user_csv_data = 'account_name,password,first_name,last_name,birthdate,email,phone,address,borrowed_book,permission\nmimi,12345,mimi,Lin,1988-09-12,mimilin@hotmail.com,0912345678,Vancouver,NA,normal\n'

class TestBookSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up class-level attributes, executed once before all tests
        cls.user_name = 'mimi'
        cls.book_name = 'One Day'

    @classmethod
    def tearDownClass(cls):
        # Clean up class-level attributes, executed once after all tests
        del cls.user_name
        del cls.book_name

    def setUp(self):
        # Set up before each test method
        self.book_system = BookSystem()

    def tearDown(self):
        # Clean up after each test method
        del self.book_system

    def mock_open_helper(self, path, *args, **kwargs):
        """Helper function to return different mock data based on file path."""
        if path == 'Librarysystem/database/book.csv':
            return mock_open(read_data=book_csv_data).return_value
        elif path == 'Librarysystem/database/user.csv':
            return mock_open(read_data=user_csv_data).return_value
        else:
            return mock_open().return_value

    @patch('builtins.input', return_value='One Day')
    @patch('builtins.open', new_callable=mock_open)
    def test_borrow_book_available(self, mock_file, mock_input):
        # Test borrowing an available book
        mock_file.side_effect = self.mock_open_helper
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.book_system.borrow_book(self.user_name)
            self.assertIn(f'Book \'{self.book_name.lower()}\' has been borrowed.', mock_stdout.getvalue())

    @patch('builtins.input', return_value='One Day')
    @patch('builtins.open', new_callable=mock_open)
    def test_return_book_success(self, mock_file, mock_input):
        # Test returning a borrowed book successfully
        mock_file.side_effect = self.mock_open_helper
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.book_system.return_book(self.user_name)
            self.assertIn('No borrowed book to return.', mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open)
    def test_get_books(self, mock_file):
        # Test getting books by title keyword
        mock_file.side_effect = self.mock_open_helper
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.book_system.get_books('one')
            self.assertIn(self.book_name, mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
