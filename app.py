from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/dormantrackerdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# Create tables
with app.app_context():
    db.create_all()

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/add_user/<username>/<email>')
def add_user(username, email):
    new_user = User(username=username, email=email)
    db.session.add(new_user)
    db.session.commit()
    return f"User {username} added successfully!"

@app.route('/users')
def get_users():
    users = User.query.all()
    user_list = [{"id": user.id, "username": user.username, "email": user.email} for user in users]
    return jsonify(user_list)

if __name__ == '__main__':
    app.run(debug=True)