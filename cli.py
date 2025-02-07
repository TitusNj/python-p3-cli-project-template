# The main entry point of the CLI.
# Displays the Main Menu options: ✅ 1. Manage Tasks → Calls tasks.py.
# ✅ 2. Manage Users → Calls users.py.
# ✅ 3. View Reports → Calls reports.py.
# ✅ 0. Exit → Exits the progr

# cli.py

from lib.task import task_menu
from lib.user import user_menu
from lib.report import reports_menu
from lib.database import init_db
import logging

# Disable SQLAlchemy logs except errors
logging.basicConfig(level=logging.ERROR)
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.pool").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.dialects").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.orm").setLevel(logging.ERROR)

def main():
    while True:
        init_db() 
        print("\nWelcome to Task Manager CLI!")
        print("1. Manage Tasks")
        print("2. Manage Users")
        print("3. View Reports")
        print("0. Exit")

        choice = input("> ")

        if choice == "1":
            task_menu()
        elif choice == "2":
            user_menu()
        elif choice == "3":
           reports_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
