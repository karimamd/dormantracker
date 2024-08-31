from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/productivity_tracker'
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

with app.app_context():
    db.create_all()

# API routes

@app.route('/category', methods=['POST'])
def create_category():
    data = request.json
    new_category = Category(name=data['name'])
    db.session.add(new_category)
    db.session.commit()
    return jsonify({'message': 'Category created successfully', 'id': new_category.id}), 201

@app.route('/task', methods=['POST'])
def create_task():
    data = request.json
    category = Category.query.get(data['category_id'])
    if not category:
        return jsonify({'message': 'Category not found'}), 404
    
    new_task = Task(name=data['name'], category=category)
    db.session.add(new_task)
    db.session.commit()
    
    for level_data in data.get('levels', []):
        new_level = TaskLevel(
            task=new_task,
            level=level_data['level'],
            description=level_data['description'],
            target_value=level_data['target_value'],
            unit=level_data.get('unit')
        )
        db.session.add(new_level)
    
    db.session.commit()
    return jsonify({'message': 'Task created successfully', 'id': new_task.id}), 201

@app.route('/progress', methods=['POST'])
def log_progress():
    data = request.json
    task = Task.query.get(data['task_id'])
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    
    new_entry = ProgressEntry(
        task=task,
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        value=data['value']
    )
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Progress logged successfully'}), 201

@app.route('/report', methods=['GET'])
def get_report():
    tasks = Task.query.all()
    report = []
    for task in tasks:
        task_report = {
            'task_name': task.name,
            'category': task.category.name,
            'levels_reached': []
        }
        for level in task.levels:
            progress = ProgressEntry.query.filter_by(task_id=task.id).order_by(ProgressEntry.date.desc()).first()
            if progress and progress.value >= level.target_value:
                task_report['levels_reached'].append({
                    'level': level.level,
                    'description': level.description
                })
        report.append(task_report)
    return jsonify(report)

if __name__ == '__main__':
    app.run(debug=True)