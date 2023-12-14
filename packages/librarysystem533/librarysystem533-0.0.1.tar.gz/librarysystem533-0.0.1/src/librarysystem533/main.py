from admin.admin_action import AdminAction
from user.user_action import UserAction

def main():
    choice = input("Please choose a login method: Admin or User (type 'Admin' or 'User'): ")

    if choice.lower() == 'admin':
        admin_authenticator = AdminAction()
        admin_authenticator.start()
    elif choice.lower() == 'user':
        user_action = UserAction()
        user_action.start()
    else:
        print("Invalid choice, please re-enter 'Admin' or 'User'.")

if __name__ == "__main__":
    main()
