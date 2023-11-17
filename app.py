from random import randint
from time import sleep

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://taskapp:taskapp@localhost:5432/taskapp'


db = SQLAlchemy(app)
migrate = Migrate(app, db)
celery = Celery('tasks', broker='pyamqp://guest:guest@localhost//')


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    status = db.Column(db.String, default="pending")


@celery.task(name='tasks.do_task')
def do_task(task_id):
    with app.app_context():
        task = Task.query.get(task_id)
        task.status = "executing"
        db.session.commit()
        sleep(randint(5, 20))
        task.status = "done"
        db.session.commit()


@app.route('/')
def index():
    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/add', methods=['POST'])    
def add():
    description = request.form['description']
    new_task = Task(description=description)
    db.session.add(new_task)
    db.session.commit()

    do_task.apply_async(args=[new_task.id], countdown=randint(5, 20))

    return redirect(url_for('index'))