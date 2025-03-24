# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 15:25:55 2025

@author: Brent
"""
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

# Update this with your own DB credentials
DATABASE_URL = "postgresql://postgres:postgres@35.237.14.240:5432/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


# Define the Task model
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    done = Column(Boolean, default=False)

    def __repr__(self):
        status = "✅" if self.done else "❌"
        return f"[{status}] {self.id}: {self.description}"


# Create the table if it doesn't exist
Base.metadata.create_all(engine)


# Command-line app functions
def add_task(description):
    task = Task(description=description)
    session.add(task)
    session.commit()
    print("Task added!")


def list_tasks():
    tasks = session.query(Task).all()
    for task in tasks:
        print(task)


def mark_done(task_id):
    task = session.query(Task).get(task_id)
    if task:
        task.done = True
        session.commit()
        print("Task marked as done.")
    else:
        print("Task not found.")


def delete_task(task_id):
    task = session.get(task_id)
    if task:
        session.delete(task)
        session.commit()
        print("Task deleted.")
    else:
        print("Task not found.")


# Simple interactive CLI
def main():
    while True:
        print("\n--- To-Do App ---")
        print("1. Add Task")
        print("2. List Tasks")
        print("3. Mark Task as Done")
        print("4. Delete Task")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            desc = input("Task description: ")
            add_task(desc)
        elif choice == "2":
            list_tasks()
        elif choice == "3":
            task_id = int(input("Task ID to mark done: "))
            mark_done(task_id)
        elif choice == "4":
            task_id = int(input("Task ID to delete: "))
            delete_task(task_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
