import os
from datetime import timedelta
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-this'
    SQLALCHEMY_DATABASE_URI =  os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:Akshay%40123@localhost/eduverse'
    SQLALCHEMY_TRACK_MODIFICATION = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-this'
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16*1024*1024
    ALLOWED_EXTENSIONS = {'pdf','doc','docx','ppt','pptx','zip'}
    

