from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from lib.database import Base, get_db
from lib.task import Task


# Uncomment this line to ensure the tables are created if needed
# Base.metadata.create_all(bind=engine)

def user_menu():
    while True:
        print("\nUser Management")
        print("1. Create a User")
        print("2. List All Users")
        print("3. Update a User")
        print("4. Delete a User")
        print("5. Back to Main Menu")

        choice = input("> ")

        if choice == "1":
            name = input("Enter your name: ")  # Ask the user for their name
            create_user(name)
        elif choice == "2":
            list_users()
        elif choice == "3":
            user_id = input("Enter the ID of the user to update: ")
            if user_id.isdigit():
                user_id = int(user_id)
                new_name = input("Enter the new name: ")
                update_user(user_id, new_name)
            else:
                print("❌ Invalid input! Please enter a valid numeric ID.")
        elif choice == "4":
            user_id = input("Enter the ID of the user to delete: ")
            if user_id.isdigit():  # Ensure it's a number
                delete_user(int(user_id))
            else:
                print("❌ Invalid input! Please enter a valid numeric ID.")
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)

    # Relationship: A user can have multiple tasks
    tasks = relationship("Task", backref="user", cascade="all, delete")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"

# ---------------- USER FUNCTIONS ---------------- #

def create_user(name):
    """Create a new user"""
    with get_db() as db:  # Use the session from the context manager
        existing_user = db.query(User).filter_by(name=name).first()
        if existing_user:
            print(f"❌ User '{name}' already exists!")
            return None
        
        user = User(name=name)
        db.add(user)
        db.commit()
        print(f"✅ User '{name}' created successfully!")
        return user


def list_users():
    """List all users"""
    with get_db() as db:
        users = db.query(User).all()
        if not users:
            print("⚠️ No users found.")
            return
        print("\n📋 Registered Users:")
        for user in users:
            print(f"🆔 {user.id} - {user.name}")

def update_user(user_id, new_name):
    """Update a user's name by ID"""
    with get_db() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.name = new_name
            db.commit()
            print(f"✅ User {user_id} updated to {new_name}.")
        else:
            print("❌ User not found.")


def delete_user(user_id):
    """Delete a user by ID"""
    with get_db() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            print(f"✅ User {user_id} deleted successfully!")
        else:
            print("❌ User not found.")

def get_user_tasks(user_id):
    with get_db() as db:
        """Get all tasks assigned to a user"""
        user = db.query(User).filter_by(id=user_id).first()
        if not user:
            print(f"❌ User with ID {user_id} not found!")
            return []
        
        tasks = db.query(Task).filter_by(user_id=user_id).all()
        if not tasks:
            print(f"⚠️ No tasks found for user {user.name}.")
            return []
        
        print(f"\n📝 Tasks for {user.name}:")
        for task in tasks:
            print(f"📌 {task.id}: {task.title} - Status: {task.status}")

        return tasks
