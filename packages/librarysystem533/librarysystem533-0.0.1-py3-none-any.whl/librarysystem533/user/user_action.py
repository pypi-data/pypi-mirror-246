from user.account_system import AccountSystem
from user.book_system import BookSystem

class UserAction:
    def __init__(self):
        self.user = None
        self.book = None
        self.borrowed_date = None
        self.account_system = AccountSystem()
        self.book_system = BookSystem()

    def start(self):
        print("Welcome to the library management system.")
        while True:
            print("\nWhat do you want to do today?")
            print("1. Log in")
            print("2. New user registration")
            print("3. Exit")

            choice = input("\nEnter a number: ")

            if choice not in ["1", "2", "3"]:
                print("Error: Invalid input")
                continue

            if choice == "3":
                print("See you next time.")
                exit(1)
            elif choice == "1":
                self.user = self.account_system.log_in()
                if self.user:
                    print(f"Welcome, {self.user}")
                    self.main_app()
            elif choice == "2":
                self.account_system.create_account()

    def main_app(self):
        while True:
            print("--------------------------")
            print("Library System ver 1.00")
            print(f"Account:\t{self.user}")
            print("--------------------------")
            print("1. Update Account Profile")
            print("2. Reset Password")
            print("3. Borrow Book")
            print("4. Return Book")
            print("5. Search Book")
            print("6. List all the Books")
            print("7. Log out")
            print("--------------------------")

            choice = input("\nEnter a number: ")

            try:
                if choice == "1":
                    self.account_system.update_profile(self.user)
                elif choice == "2":
                    self.account_system.reset_password(self.user)
                elif choice == "3":
                    self.book_system.borrow_book(self.user)
                elif choice == "4":
                    self.book_system.return_book(self.user)
                elif choice == "5":
                    search = input("\nEnter the book title or author you want to search: ")
                    self.book_system.get_books(search)
                elif choice == "6":
                    self.book_system.get_books()
                elif choice == "7":
                    self.account_system.log_out(self.user)
                    return
                else:
                    print("Error: Invalid input")
            except Exception as e:
                print(f"An error occurred: {e}")
                break  # Optionally break the loop on exception