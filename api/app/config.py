import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif', 'pdf'}

    # Database configuration
    DB_HOST = 'localhost'
    DB_USER = 'root'
    DB_PASSWORD = 'rootroot'
    DB_NAME = 'floor_plans_db'
