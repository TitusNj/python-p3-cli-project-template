from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from lib.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    due_date = Column(Date, nullable=False)
    status = Column(String, default="Pending")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Linking to Users table

    def __repr__(self):
        return f"Task(id={self.id}, title={self.title}, status={self.status})"
