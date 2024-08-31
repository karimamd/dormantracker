from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/dormantrackerdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    tasks = db.relationship('Task', back_populates='category')

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    category = db.relationship('Category', back_populates='tasks')
    levels = db.relationship('TaskLevel', back_populates='task')
    progress_entries = db.relationship('ProgressEntry', back_populates='task')

class TaskLevel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    level = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(200))
    target_value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(50))
    task = db.relationship('Task', back_populates='levels')

class ProgressEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    value = db.Column(db.Float, nullable=False)
    task = db.relationship('Task', back_populates='progress_entries')

@app.route('/')
def index():
    categories = Category.query.all()
    tasks = Task.query.all()
    return render_template('index.html', categories=categories, tasks=tasks)

@app.route('/add_category', methods=['POST'])
def add_category():
    name = request.form['name']
    new_category = Category(name=name)
    db.session.add(new_category)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_task', methods=['POST'])
def add_task():
    name = request.form['name']
    category_id = request.form['category_id']
    new_task = Task(name=name, category_id=category_id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/add_level', methods=['POST'])
def add_level():
    task_id = request.form['task_id']
    level = request.form['level']
    description = request.form['description']
    target_value = request.form['target_value']
    unit = request.form['unit']
    new_level = TaskLevel(task_id=task_id, level=level, description=description, target_value=target_value, unit=unit)
    db.session.add(new_level)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/log_progress', methods=['POST'])
def log_progress():
    task_id = request.form['task_id']
    date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    value = request.form['value']
    new_entry = ProgressEntry(task_id=task_id, date=date, value=value)
    db.session.add(new_entry)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)