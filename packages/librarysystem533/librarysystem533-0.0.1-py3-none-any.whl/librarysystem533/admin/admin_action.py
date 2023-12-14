import sys, os
import csv
from admin.user_management_system import UserManagementSystem
from admin.book_management_system import BookManagementSystem

admin_filename = "Librarysystem/database/administrator.csv"
user_filename = "Librarysystem/database/user.csv"
book_filename = "Librarysystem/database/book.csv"

class UserManagementError(Exception):
    """Exception raised for errors in the user management system."""
    def __init__(self, message="Error in user management"):
        super().__init__(message)

class BookManagementError(Exception):
    """Exception raised for errors in the book management system."""
    def __init__(self, message="Error in book management"):
        super().__init__(message)

class AdminAction():
    def __init__(self):
        self.admins_filename = admin_filename
        self.logged_in = False

    def login_admin(self):
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        try:
            with open(self.admins_filename, newline='', encoding='utf-8-sig') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row['user_name'] == username and row['password'] == password:
                        print(f"Login successful for {row['title']}.")
                        self.logged_in = True
                        return row['title']
            print("Invalid username or password.")
        except FileNotFoundError:
            print(f"Error: File '{self.admins_filename}' not found.")
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return None

    def logout(self):
        print("Logging out...")
        self.logged_in = False

    def main_interface(self):
        while True:
            print("1: User Management\n2: Book Management\n3: Logout")
            choice = input("Enter your choice: ")

            if choice == '1':
                self.user_management_interface()
            elif choice == '2':
                self.book_management_interface()
            elif choice == '3':
                self.logout()
                break
            else:
                print("Invalid choice, please try again.")

    def user_management_interface(self):
        try:
            user_system = UserManagementSystem()
            user_system.user_interface()
        except Exception as e:
            raise UserManagementError(f"Error in user management: {e}")

    def book_management_interface(self):
        try:
            book_system = BookManagementSystem()
            book_system.book_interface()
        except Exception as e:
            raise BookManagementError(f"Error in book management: {e}")

    def start(self):
        admin_title = self.login_admin()
        if self.logged_in:
            print(f"Welcome {admin_title}.")
            self.main_interface()
