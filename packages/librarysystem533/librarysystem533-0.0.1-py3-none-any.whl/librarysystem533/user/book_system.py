import csv
from datetime import datetime

user_filename = "Librarysystem/database/user.csv"
book_filename = "Librarysystem/database/book.csv"

class BookSystem:
    def __init__(self):
        self.book_csv_file_path = book_filename
        self.user_csv_file_path = user_filename

    def borrow_book(self, user_account):
        """Allows a user to borrow a book."""
        book_title = input("Enter the title of the book you want to borrow: ").strip().lower()

        # Check if the user already has a borrowed book
        if self.user_has_borrowed_book(user_account):
            print(f"You already have a borrowed book. Please return it first.")
            return

        # Find and borrow the book
        books = self.read_books_csv()
        for book in books:
            if book['title'].lower() == book_title and book['is_available'].lower() == "yes":
                book['is_available'] = "no"
                book['borrowed_user'] = user_account
                book['times_borrowed'] = str(int(book['times_borrowed']) + 1)
                book['last_borrow_date'] = datetime.now().strftime("%Y-%m-%d")
                self.write_books_csv(books)
                self.update_user_borrowed_book(user_account, book_title)
                print(f"Book '{book_title}' has been borrowed.")
                return
        print("Book not available or does not exist.")

    def return_book(self, user_account):
        """Allows a user to return a book."""
        books = self.read_books_csv()
        user_info = self.get_user_info(user_account)
        if not user_info or user_info['borrowed_book'] == "NA":
            print("No borrowed book to return.")
            return

        for book in books:
            if book['title'].lower() == user_info['borrowed_book'].lower() and book['borrowed_user'] == user_account:
                book['is_available'] = "yes"
                book['borrowed_user'] = ""
                book['return_date'] = datetime.now().strftime("%Y-%m-%d")
                self.write_books_csv(books)
                self.update_user_borrowed_book(user_account, "NA")
                print(f"Book '{book['title']}' has been returned.")
                return

    def get_books(self, search_term=None):
        """Lists all books or searches for books by a given term."""
        books = self.read_books_csv()
        print(f"{'ID':<10} {'Title':<30} {'Author':<20} {'Year':<6} {'Available':<10}")
        for book in books:
            if search_term and search_term.lower() not in book['title'].lower() and search_term.lower() not in book['author'].lower():
                continue
            print(f"{book['book_id']:<10} {book['title']:<30} {book['author']:<20} {book['published_year']:<6} {book['is_available']:<10}")

    def user_has_borrowed_book(self, user_account):
        """Checks if a user currently has a borrowed book."""
        user_info = self.get_user_info(user_account)
        return user_info and user_info['borrowed_book'] != "NA"

    def get_user_info(self, user_account):
        """Gets information about a user."""
        with open(self.user_csv_file_path, 'r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for user in reader:
                if user['account_name'] == user_account:
                    return user
        return None

    def update_user_borrowed_book(self, user_account, book_title):
        """Updates the borrowed book for a user."""
        users = self.read_users_csv()
        for user in users:
            if user['account_name'] == user_account:
                user['borrowed_book'] = book_title
                break
        self.write_users_csv(users)

    def read_books_csv(self):
        """Reads books data from the CSV file."""
        with open(self.book_csv_file_path, 'r', newline='', encoding='utf-8-sig') as file:
            return list(csv.DictReader(file))

    def write_books_csv(self, books):
        """Writes books data back to the CSV file."""
        with open(self.book_csv_file_path, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=books[0].keys())
            writer.writeheader()
            writer.writerows(books)

    def read_users_csv(self):
        """Reads users data from the CSV file."""
        with open(self.user_csv_file_path, 'r', newline='', encoding='utf-8-sig') as file:
            return list(csv.DictReader(file))

    def write_users_csv(self, users):
        """Writes users data back to the CSV file."""
        with open(self.user_csv_file_path, 'w', newline='', encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=users[0].keys())
            writer.writeheader()
            writer.writerows(users)
