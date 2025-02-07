import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from contextlib import contextmanager

# Define the database URL (SQLite for simplicity, can be changed to PostgreSQL/MySQL)
DATABASE_URL = "sqlite:///task_manager.db"  # Can be an environment variable for flexibility

# Create the database engine
engine = create_engine(DATABASE_URL, echo=False, future=True)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the Base class for models
Base = declarative_base()

# Suppress SQLAlchemy logging
logging.basicConfig(level=logging.ERROR)
logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
logging.getLogger("sqlalchemy.pool").setLevel(logging.WARNING)
logging.getLogger("sqlalchemy.dialects").setLevel(logging.ERROR)

# Function to initialize the database
def init_db():
    """Creates all tables in the database"""
    from lib.user import User  # Import models
    from lib.task import Task  # Import models
    Base.metadata.create_all(bind=engine)  # Create tables in the database
    # print("✅ Database initialized successfully!")

# Session management (context manager)
@contextmanager
def get_db():
    """Yield a session to be used for database transactions"""
    db = SessionLocal()
    try:
        yield db  # Use the session
    finally:
        db.close()  # Ensure the session is closed after use

