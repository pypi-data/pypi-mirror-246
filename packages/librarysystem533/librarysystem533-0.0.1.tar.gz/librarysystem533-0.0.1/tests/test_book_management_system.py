import unittest
from unittest.mock import patch, mock_open, MagicMock
from admin.book_management_system import BookManagementSystem
import io

# Test data for books in CSV format
book_csv_data = 'book_id,title,author,published_year,ISBN,is_available,First_entry_date,times_borrowed,borrowed_user,last_borrow_date,last_return_date\n1,One Day,David Nicholls,2009,978-0274808465,yes,2023/1/1,3,,2023-12-04,2023-12-04\n'

class TestBookManagementSystem(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up class-level attributes, executed once before all tests
        cls.book_name = 'One Day'

    @classmethod
    def tearDownClass(cls):
        # Clean up class-level attributes, executed once after all tests
        del cls.book_name

    def setUp(self):
        # Set up before each test method
        self.book_system = BookManagementSystem()

    def tearDown(self):
        # Clean up after each test method
        del self.book_system

    @patch('builtins.input', return_value='David Nicholls')
    @patch('builtins.open', new_callable=mock_open, read_data=book_csv_data)
    def test_search_books(self, mock_file, mock_input):
        # Test searching books by author
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.book_system.search_books()
            self.assertIn('David Nicholls', mock_stdout.getvalue())

    @patch('builtins.open', new_callable=mock_open, read_data=book_csv_data)
    def test_list_books(self, mock_file):
        # Test listing all books
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.book_system.list_books()
            self.assertIn(self.book_name, mock_stdout.getvalue())

    @patch('builtins.input', side_effect=['New Book', 'New Author', '2023', '1234567890'])
    @patch('builtins.open', new_callable=mock_open, read_data=book_csv_data)
    def test_add_book(self, mock_file, mock_input):
        # Test adding a new book
        with patch('csv.DictWriter.writerow', new_callable=MagicMock) as mock_write_row:
            self.book_system.add_book()
            mock_write_row.assert_called()

    @patch('builtins.input', return_value='1')
    @patch('builtins.open', new_callable=mock_open, read_data=book_csv_data)
    def test_remove_book(self, mock_file, mock_input):
        # Test removing a book
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.book_system.remove_book()
            self.assertIn('Book removed successfully.', mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
