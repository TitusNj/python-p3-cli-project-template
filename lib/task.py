# Handles task-related operations: ✅ Create a Task.
# ✅ List All Tasks.
# ✅ Update a Task.
# ✅ Delete a Task.
# ✅ Mark Task as Complete.


from lib.database import get_db
from lib.task_model import Task  # Importing Task model
from datetime import datetime

def task_menu():
    with get_db() as db:
        while True:
            print("\nTask Management")
            print("1. Create a Task")
            print("2. List All Tasks")
            print("3. Update a Task")
            print("4. Delete a Task")
            print("5. Mark Task as Complete")
            print("6. Back to Main Menu")
            print("0. Exit")

            choice = input("> ")

            if choice == "1":
                create_task()
            elif choice == "2":
                list_tasks()
            elif choice == "3":
                update_task()
            elif choice == "4":
                delete_task()
            elif choice == "5":
                mark_task_complete()
            elif choice == "6":
                break
            elif choice == "0":
                exit()
            else:
                print("Invalid choice. Please try again.")

def create_task():
    with get_db() as db:
        title = input("Enter the task's title: ")
        description = input("Enter the task's description: ")
        due_date = input("Enter the due date (YYYY-MM-DD): ")
        user_id = input("Enter the user's ID: ")

        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
            new_task = Task(title=title, description=description, due_date=due_date, user_id=user_id)
            db.add(new_task)
            db.commit()
            print(f"✅ Task created: {new_task}")
        except Exception as e:
            print(f"Error creating task: {e}")

def list_tasks():
    with get_db() as db:
        tasks = db.query(Task).all()
        if tasks:
            print("\n📋 Task List:")
            for task in tasks:
                print(f"🆔 {task.id} | 📌 {task.title} | 📅 {task.due_date} | ✅ Status: {task.status}")
        else:
            print("No tasks found.")

def update_task():
    with get_db() as db:
        task_id = input("Enter the Task ID to update: ")
        task = db.query(Task).filter_by(id=task_id).first()

        if task:
            task.title = input(f"Enter new title ({task.title}): ") or task.title
            task.description = input(f"Enter new description ({task.description}): ") or task.description
            due_date = input(f"Enter new due date ({task.due_date}, YYYY-MM-DD): ")
            if due_date:
                task.due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

            db.commit()
            print(f"✅ Task updated: {task}")
        else:
            print("Task not found.")

def delete_task():
    with get_db() as db:
        task_id = input("Enter the Task ID to delete: ")
        task = db.query(Task).filter_by(id=task_id).first()

        if task:
            db.delete(task)
            db.commit()
            print(f"🗑 Task deleted: {task}")
        else:
            print("Task not found.")

def mark_task_complete():
    with get_db() as db:
        task_id = input("Enter the Task ID to mark as complete: ")
        task = db.query(Task).filter_by(id=task_id).first()

        if task:
            task.status = "Completed"
            db.commit()
            print(f"🎉 Task marked as complete: {task}")
        else:
            print("Task not found.")

if __name__ == "__main__":
    task_menu()
