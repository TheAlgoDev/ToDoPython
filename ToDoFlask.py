# -*- coding: utf-8 -*-
"""
Created on Mon Mar 24 15:25:55 2025

@author: Brent
"""
from flask import Flask, render_template_string, request, redirect, url_for

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, declarative_base

# Update this with your own DB credentials
DATABASE_URL = "postgresql://postgres:postgres@35.237.14.240:5432/postgres"

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


# Define Task model
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    done = Column(Boolean, default=False)

Base.metadata.create_all(engine)

# Flask app
app = Flask(__name__)

# HTML Template
HTML = '''
<!doctype html>
<title>Todo List</title>
<h1>My To-Do List</h1>
<form method="POST" action="/add">
  <input name="description" placeholder="New task" required>
  <button type="submit">Add</button>
</form>
<ul>
  {% for task in tasks %}
    <li>
      {% if task.done %}
        <s>{{ task.description }}</s>
      {% else %}
        {{ task.description }}
      {% endif %}
      [<a href="{{ url_for('mark_done', task_id=task.id) }}">done</a>]
      [<a href="{{ url_for('delete_task', task_id=task.id) }}">delete</a>]
    </li>
  {% endfor %}
</ul>
'''

@app.route('/')
def index():
    tasks = session.query(Task).all()
    return render_template_string(HTML, tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    desc = request.form['description']
    task = Task(description=desc)
    session.add(task)
    session.commit()
    return redirect(url_for('index'))

@app.route('/done/<int:task_id>')
def mark_done(task_id):
    task = session.query(Task).get(task_id)
    if task:
        task.done = True
        session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = session.query(Task).get(task_id)
    if task:
        session.delete(task)
        session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=False)