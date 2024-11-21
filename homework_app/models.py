from homework_app import db

# Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    class_name = db.Column(db.String(50), nullable=False)
    homeworks = db.relationship('Homework', backref='student', lazy=True)

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    homework_title = db.Column(db.String(100), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)