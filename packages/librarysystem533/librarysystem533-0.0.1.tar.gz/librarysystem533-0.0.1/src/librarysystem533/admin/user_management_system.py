import csv
import sys
import matplotlib.pyplot as plt


user_filename = "Librarysystem/database/user.csv"

class CSVFileManager:
    def __init__(self, filename):
        self.filename = filename

    def read_from_csv(self):
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8-sig') as csvfile:
                return list(csv.DictReader(csvfile))
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            return []
        except csv.Error as e:
            print(f"Error reading CSV file: {e}")
            return []
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return []

    def write_to_csv(self, data):
        if not data:
            return
        try:
            with open(self.filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
        except csv.Error as e:
            print(f"Error writing to CSV file: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


class UserManagementSystem(CSVFileManager):
    def __init__(self):
        super().__init__(user_filename)

    def delete_user(self):
        account_name_to_delete = input("Enter the account name of the user to delete: ")

        # Open the CSV file and read the users
        users = self.read_from_csv()

        # Check if the user exists in the list
        user_found = any(user['account_name'] == account_name_to_delete for user in users)

        if user_found:
            # Exclude the user to be deleted
            updated_users = [user for user in users if user['account_name'] != account_name_to_delete]
            self.write_to_csv(updated_users)
            print(f"User '{account_name_to_delete}' has been deleted.")
        else:
            print(f"No user found with the account name '{account_name_to_delete}'.")

    def update_permissions(self):
        account_name_to_update = input("Enter the account name to update permissions: ")
        new_permission = input("Enter the new permission level ('prohibit' or 'normal'): ")

        # Ensure valid permission input
        if new_permission not in ['prohibit', 'normal']:
            print("Invalid permission level.")
            return

        users = self.read_from_csv()
        for user in users:
            if user['account_name'] == account_name_to_update:
                user['permission'] = new_permission
                self.write_to_csv(users)
                print(f"Permissions updated for user '{account_name_to_update}'.")
                return

        print(f"No user found with the account name '{account_name_to_update}'.")

    def user_details(self):
        account_name_to_find = input("Enter the account name to retrieve details: ")

        users = self.read_from_csv()
        for user in users:
            if user['account_name'] == account_name_to_find:
                print("User Details:")
                for key, value in user.items():
                    print(f"{key}: {value}")
                return

        print(f"No user found with the account name '{account_name_to_find}'.")

    def view_user_activity(self):
        users = self.read_from_csv()
        borrowed_count = sum(1 for user in users if user['borrowed_book'].upper() != 'NA')
        not_borrowed_count = len(users) - borrowed_count

        labels = ['Borrowed Books', 'No Books Borrowed']
        sizes = [borrowed_count, not_borrowed_count]
        colors = ['lightcoral', 'lightskyblue']
        explode = (0.1, 0)  # explode the 1st slice (borrowed)

        plt.figure(figsize=(8, 6))
        plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
        plt.title('Book Borrowing Status')
        plt.axis('equal')
        plt.show()

    def user_interface(self):
        while True:
            print("1: Delete User Accounts\n2: Modify User Permissions\n3: Retrieve User Account Details\n4: Monitor User Activity\n5: Logout")
            choice = input("Enter your choice: ")
            action_map = {
                '1': self.delete_user,
                '2': self.update_permissions,
                '3': self.user_details,
                '4': self.view_user_activity,
                '5': sys.exit
            }

            action = action_map.get(choice)
            if action:
                action()
            else:
                print("Invalid choice, please try again.")
