from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# สร้าง instance ของ Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'homework_app/uploads'  # กำหนดโฟลเดอร์อัปโหลดไฟล์
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}

# สร้าง SQLAlchemy และ Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Import Blueprints หรือไฟล์อื่นๆ
from homework_app import models, routes
