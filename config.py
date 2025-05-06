import os
from werkzeug.security import generate_password_hash

class Config:
    SECRET_KEY = 'anton'  

    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'password!'  
    MYSQL_DB = 'review_web'

    DEBUG = True
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'zip', 'pdf', 'txt'}

    ROLES = {
        'student': 'student',
        'reviewer': 'reviewer',
        'admin': 'admin'
    }

os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)