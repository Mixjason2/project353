from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime, timedelta
import os
from werkzeug.utils import secure_filename
import requests
from apscheduler.schedulers.background import BackgroundScheduler

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # Database URI
app.config['UPLOAD_FOLDER'] = 'uploads/'  # Folder for file uploads
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'docx', 'txt', 'jpg', 'png'}  # Allowed file extensions

# Initialize SQLAlchemy and Flask-Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)  # Initialize Migrate after the app instance

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
    filename = db.Column(db.String(200), nullable=False)  # This line is critical
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    
# Helper functions
def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def send_line_notify(message):
    """Send a message via Line Notify."""
    token = 'YOUR_LINE_NOTIFY_ACCESS_TOKEN'  # Replace with your Line Notify Token
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    payload = {'message': message}
    requests.post('https://notify-api.line.me/api/notify', headers=headers, data=payload)

def check_homework_due():
    """Check if homework is due in the next 2 days and send a notification."""
    now = datetime.now()
    upcoming_homeworks = Homework.query.filter(Homework.due_date <= now + timedelta(days=2)).all()
    for homework in upcoming_homeworks:
        student = homework.student
        message = f"การบ้าน '{homework.homework_title}' ของ {student.name} ใกล้ถึงกำหนดส่งแล้ว"
        send_line_notify(message)

# Schedule background job to check homework due dates every 24 hours
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_homework_due, trigger="interval", hours=24)
scheduler.start()

# Routes
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        class_name = request.form['class_name']
        new_student = Student(name=name, email=email, class_name=class_name)
        db.session.add(new_student)
        db.session.commit()
        flash('เพิ่มนักเรียนเรียบร้อยแล้ว', 'success')
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/set_homework', methods=['GET', 'POST'])
def set_homework():
    if request.method == 'POST':
        homework_title = request.form['homework_title']
        student_id = request.form['student_id']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            new_homework = Homework(
                homework_title=homework_title,
                due_date=due_date,
                filename=filename,
                student_id=student_id
            )
            db.session.add(new_homework)
            db.session.commit()
            flash('การบ้านถูกเพิ่มเรียบร้อยแล้ว', 'success')
            return redirect(url_for('index'))
        else:
            flash('รูปแบบไฟล์ไม่ถูกต้อง', 'error')
    students = Student.query.all()
    return render_template('set_homework.html', students=students)

@app.route('/view_homeworks')
def view_homeworks():
    homeworks = Homework.query.all()
    return render_template('view_homeworks.html', homeworks=homeworks)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Initialize the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
