import csv
from admin.user_management_system import CSVFileManager

book_filename = "Librarysystem/database/book.csv"

class BookManagementSystem(CSVFileManager):
    def __init__(self):
        super().__init__(book_filename)
        self.book_filename = book_filename

    def search_books(self):
        search_query = input("Enter search term for any book attribute: ").lower()
        found_books = self.find_books_by_query(search_query)

        if found_books:
            print("Search Results:")
            for book in found_books:
                print(", ".join(f"{key}: {value}" for key, value in book.items()))
        else:
            print("No books found matching the query.")

    def list_books(self):
        try:
            with open(self.book_filename, newline="", encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                print("List of Books:")
                for row in reader:
                    print(f"{row['book_id']}: {row['title']} by {row['author']} (Published: {row['published_year']})")
        except FileNotFoundError:
            print(f"Error: File '{self.book_filename}' not found.")
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")

    def add_book(self):
        new_book = self.collect_book_details()
        self.append_book_to_csv(new_book)
        print(f"Book added successfully. The new book ID is: {new_book['book_id']}")

    def remove_book(self):
        book_id_to_remove = input("Enter the ID of the book to remove: ")
        self.delete_book_from_csv(book_id_to_remove)
        print("Book removed successfully.")

    def find_books_by_query(self, query):
        with open(self.book_filename, newline="", encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            return [row for row in reader if query in str(row).lower()]

    def collect_book_details(self):
        # Read existing data to determine the next book_id
        next_id = self.get_next_book_id()
        return {
            "book_id": str(next_id),
            "title": input("Enter book title: "),
            "author": input("Enter author's name: "),
            "published_year": input("Enter the year of publication: "),
            "ISBN": input("Enter the ISBN number: "),
        }

    def append_book_to_csv(self, book):
        with open(self.book_filename, "a", newline="", encoding='utf-8-sig') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=book.keys())
            if csvfile.tell() == 0:  # If file is empty, write header
                writer.writeheader()
            writer.writerow(book)

    def delete_book_from_csv(self, book_id):
        books = self.read_from_csv()
        updated_books = [book for book in books if book['book_id'] != book_id]
        self.write_to_csv(updated_books)

    def get_next_book_id(self):
        books = self.read_from_csv()
        if not books:
            return 1
        return max(int(book['book_id']) for book in books) + 1

    def book_interface(self):
        while True:
            print("1: Search Books\n2: List Books\n3: Add Book\n4: Remove Book\n5: Logout")
            choice = input("Enter your choice: ")
            action_map = {
                '1': self.search_books,
                '2': self.list_books,
                '3': self.add_book,
                '4': self.remove_book,
                '5': exit
            }

            action = action_map.get(choice)
            if action:
                action()
            else:
                print("Invalid choice, please try again.")
