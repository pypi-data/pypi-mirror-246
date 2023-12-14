import csv

user_filename = "Librarysystem/database/user.csv"

class AccountSystem:
    def __init__(self):
        self.csv_file_path = user_filename

    def create_account(self):
        """Creates a new user account."""
        account_name = input("Enter account name: ")
        try:
            if self.account_exists(account_name):
                print("Account already exists.")
                return

            password = input("Enter password: ")
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            birthdate = input("Enter birthdate (YYYY-MM-DD): ")
            email = input("Enter email: ")
            phone = input("Enter phone number: ")
            address = input("Enter address: ")

            user_data = {
                "account_name": account_name,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "birthdate": birthdate,
                "email": email,
                "phone": phone,
                "address": address,
                "borrowed_book": "NA",  # default none
                "permission": "normal",
            }

            with open(self.csv_file_path, "a", newline="", encoding='utf-8-sig') as file:
                writer = csv.DictWriter(file, fieldnames=user_data.keys())
                if file.tell() == 0:  # If file is empty, write header
                    writer.writeheader()
                writer.writerow(user_data)
            print("Account created successfully.")
        except FileNotFoundError:
            print(f"Error: File '{self.csv_file_path}' not found.")
        except csv.Error as e:
            print(f"Error processing CSV file: {e}")

    def update_profile(self, account_name):
        """Updates a user's profile information."""
        print("What do you want to update?")
        print("1. Email")
        print("2. Phone")
        print("3. Address")
        choice = input("Choice: ")

        if choice not in ["1", "2", "3"]:
            print("Invalid choice.")
            return

        new_data = input("Enter new data: ")
        column_name = {"1": "email", "2": "phone", "3": "address"}[choice]

        rows = self.read_csv()
        for row in rows:
            if row['account_name'] == account_name:
                row[column_name] = new_data
                break

        self.write_csv(rows)
        print("Profile updated successfully.")

    def reset_password(self, account_name):
        """Resets a user's password."""
        new_password = input("Enter new password: ")
        confirm_password = input("Confirm new password: ")

        if new_password != confirm_password:
            print("Passwords do not match!")
            return

        rows = self.read_csv()
        for row in rows:
            if row['account_name'] == account_name:
                row['password'] = new_password
                break

        self.write_csv(rows)
        print("Password has been reset successfully.")

    def log_in(self):
        """Handles user login."""
        account_name = input("Enter your account name: ")
        password = input("Enter your password: ")

        if self.validate_login(account_name, password):
            print("Logged in successfully.")
            return account_name
        else:
            print("Invalid account name or password.")
            return None

    def log_out(self, account_name):
        """Handles user logout."""
        print(f"User {account_name} logged out.")

    def account_exists(self, account_name):
        """Checks if an account already exists."""
        try:
            with open(self.csv_file_path, "r", encoding='utf-8-sig') as file:
                reader = csv.reader(file)
                return any(row[0] == account_name for row in reader)
        except FileNotFoundError:
            print(f"Error: File '{self.csv_file_path}' not found.")
            return False
        except csv.Error as e:
            print(f"Error processing CSV file: {e}")
            return False

    def validate_login(self, account_name, password):
        """Validates user credentials."""
        with open(self.csv_file_path, "r", encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            return any(row['account_name'] == account_name and row['password'] == password for row in reader)

    def read_csv(self):
        """Reads data from the CSV file."""
        with open(self.csv_file_path, "r", newline="", encoding='utf-8-sig') as file:
            return list(csv.DictReader(file))

    def write_csv(self, rows):
        """Writes data back to the CSV file."""
        with open(self.csv_file_path, "w", newline="", encoding='utf-8-sig') as file:
            writer = csv.DictWriter(file, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)
