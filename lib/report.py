# Handles task analytics: ✅ View completed vs. pending tasks.
# ✅ List overdue tasks.
# ✅ Generate a user-task summary.
# lib/reports.py

from lib.task import Task
from lib.user import User
from lib.database import get_db
from datetime import date
from tabulate import tabulate  # Install with `pip install tabulate`

def view_completed_tasks():
    with get_db() as db:
        """Displays all completed tasks."""
        completed_tasks = db.query(Task).filter(Task.status == "Completed").all()
        if completed_tasks:
            table = [[task.id, task.title, task.due_date, task.user_id] for task in completed_tasks]
            print("\n✅ Completed Tasks:")
            print(tabulate(table, headers=["ID", "Title", "Due Date", "User ID"], tablefmt="grid"))
        else:
            print("\n❌ No completed tasks found.")


def view_pending_tasks():
    with get_db() as db:
        """Displays all pending tasks."""
        pending_tasks = db.query(Task).filter(Task.status == "Pending").all()
        if pending_tasks:
            table = [[task.id, task.title, task.due_date, task.user_id] for task in pending_tasks]
            print("\n⏳ Pending Tasks:")
            print(tabulate(table, headers=["ID", "Title", "Due Date", "User ID"], tablefmt="grid"))
        else:
            print("\n✅ No pending tasks! All caught up!")  


def view_overdue_tasks():
    with get_db() as db:
        """Displays all overdue tasks."""
        today = date.today()
        overdue_tasks = db.query(Task).filter(Task.status == "Pending", Task.due_date < today).all()
        if overdue_tasks:
            table = [[task.id, task.title, task.due_date, task.user_id] for task in overdue_tasks]
            print("\n⚠️ Overdue Tasks:")
            print(tabulate(table, headers=["ID", "Title", "Due Date", "User ID"], tablefmt="grid"))
        else:
            print("\n🎉 No overdue tasks!")


def view_user_task_summary():
    with get_db() as db:
        """Displays a summary of tasks per user."""
        users = db.query(User).all()
        summary_data = []

        for user in users:
            total_tasks = db.query(Task).filter(Task.user_id == user.id).count()
            completed_tasks = db.query(Task).filter(Task.user_id == user.id, Task.status == "Completed").count()
            pending_tasks = total_tasks - completed_tasks
            summary_data.append([user.id, user.name, total_tasks, completed_tasks, pending_tasks])

        if summary_data:
            print("\n📊 User Task Summary:")
            print(tabulate(summary_data, headers=["User ID", "Name", "Total Tasks", "Completed", "Pending"], tablefmt="grid"))
        else:
            print("\n❌ No users or tasks found!")


def reports_menu():
    """CLI Menu for Viewing Reports"""
    while True:
        print("\n📌 Reports Menu")
        print("1. View Completed Tasks")
        print("2. View Pending Tasks")
        print("3. View Overdue Tasks")
        print("4. User Task Summary")
        print("5. Back to Main Menu")
        
        choice = input("> ")

        if choice == "1":
            view_completed_tasks()
        elif choice == "2":
            view_pending_tasks()
        elif choice == "3":
            view_overdue_tasks()
        elif choice == "4":
            view_user_task_summary()
        elif choice == "5":
            print("\nReturning to Main Menu...")
            break
        else:
            print("\n❌ Invalid choice, try again.")

if __name__ == "__main__":
    reports_menu()
