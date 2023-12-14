import unittest
from unittest.mock import patch, mock_open, MagicMock
import csv
import io
from admin.user_management_system import CSVFileManager

class TestCSVFileManager(unittest.TestCase):
        
    @classmethod
    def setUpClass(cls):
        # Set up class-wide attributes
        cls.filename = "test.csv"
        cls.sample_data = [{'name': 'Alice', 'age': '30'}, {'name': 'Bob', 'age': '25'}]

    @classmethod
    def tearDownClass(cls):
        # Clean up class-wide attributes after all tests are done
        del cls.filename
        del cls.sample_data

    def setUp(self):
        # Set up before each test method
        self.manager = CSVFileManager(self.filename)

    def tearDown(self):
        # Teardown method for each test method
        del self.manager
        
    def test_read_from_csv_success(self):
        # Test reading from a CSV file successfully
        mock_csv_data = "name,age\nAlice,30\nBob,25\n"
        with patch('builtins.open', new_callable=mock_open, read_data=mock_csv_data):
            result = self.manager.read_from_csv()
            self.assertEqual(len(result), 2)  # Expecting two rows
            self.assertEqual(result[0]['name'], 'Alice')

    def test_read_from_csv_file_not_found(self):
        # Test reading from a non-existent CSV file
        with patch('builtins.open', side_effect=FileNotFoundError), \
                patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            result = self.manager.read_from_csv()
            self.assertEqual(result, [])
            self.assertIn(f"Error: File '{self.filename}' not found.", mock_stdout.getvalue())

    def test_read_from_csv_csv_error(self):
        # Test handling csv.Error while reading
        with patch('csv.DictReader', side_effect=csv.Error), \
             patch('builtins.open', mock_open()), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            result = self.manager.read_from_csv()
            self.assertEqual(result, [])
            self.assertIn("Error reading CSV file:", mock_stdout.getvalue())

    def test_write_to_csv_success(self):
        # Test writing to a CSV file successfully
        with patch('builtins.open', new_callable=mock_open()) as mock_file:
            self.manager.write_to_csv(self.sample_data)
            mock_file.assert_called_once_with(self.filename, 'w', newline='', encoding='utf-8-sig')

    def test_write_to_csv_file_not_found(self):
        # Test writing to a non-existent CSV file
        with patch('builtins.open', side_effect=FileNotFoundError), \
                patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.manager.write_to_csv(self.sample_data)
            self.assertIn(f"Error: File '{self.filename}' not found.", mock_stdout.getvalue())
    
    def test_write_to_csv_csv_error(self):
        # Test handling csv.Error while writing
        mock_file = mock_open()
        with patch('builtins.open', mock_file), \
             patch('csv.DictWriter', MagicMock(side_effect=csv.Error)), \
             patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            self.manager.write_to_csv(self.sample_data)
            self.assertIn("Error writing to CSV file:", mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
