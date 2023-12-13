# test_user_subpackage.py

import sys
import os

# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from user.client import client, new_user_registration, existing_user_login
from user.admin import admin, admin_login, admin_operations

def main():
    # Example of using the client module
    print("Creating a new user:")
    new_user = new_user_registration()
    print("New user details:", new_user.show_information())

    # Example of using the admin module
    admins_dict = {1: admin("Admin1", 1, 1234)}  # Replace with your actual admin details
    clients_dict = {new_user.name: new_user}  # Assume new_user is added to clients_dict

    print("\nAdmin Login:")
    admin_login(admins_dict, clients_dict)

    # Example of admin operations
    if 'admin' in locals():
        print("\nAdmin Operations:")
        admin_operations(admin, clients_dict)

    # Example of existing user login
    print("\nExisting User Login:")
    existing_user = existing_user_login(clients_dict)
    if existing_user:
        print("Logged in user details:", existing_user.show_information())

if __name__ == "__main__":
    main()
