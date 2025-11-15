from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
db = SQLAlchemy()
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable = False)
    email = db.Column(db.String(100),unique = True,nullable = False)
    password = db.Column(db.String(255),nullable = False)
    student_id = db.Column(db.String(50),unique = True)
    department = db.Column(db.String(100))
    created_at = db.Column(db.DateTime,default = datetime.utcnow)
    materials = db.relationship('Material',backref='uploader',lazy=True)
    threads = db.relationship('ForumThread',backref='author',lazy=True)
    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'student_id':self.student_id,
            'department': self.department
        }
    
class Material(db.Model):
    __tablename__ = 'materials'
    id = db.Column(db.Integer,primary_keys = True)
    title = db.Column(db.String(200),nullable = False)
    description = db.Column(db.Text)
    subject = db.Column(db.String(50))
    file_type = db.Column(db.String(10))
    file_path = db.Column(db.String(500))
    file_size = db.Column(db.String(20))
    year = db.Column(db.String(10))
    uploaded_by = db.Column(db.Integer,db.ForeignKey('users.id'))
    downloads = db.Column(db.Integer,default = 0)
    views = db.Column(db.Integer,default = 0)
    created_at = db.Column(db.DateTime,default = datetime.utcnow)
    def to_dict(self):
        return {
            'id':self.id,
            'title':self.title,
            'description':self.description,
            'subject':self.subject,
            'file_type':self.file_type,
            'file_size':self.file_type,
            'year':self.year,
            'downloads':self.downloads,
            'views':self.views,
            'upload_date': self.created_at.strftime('%Y-%m-%d'),
            'uploader_name': self.uploader.name if self.uploader else 'Unknown'

        }
class ForumThread(db.Model):
    __tablename__ = 'forum_threads'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    tags = db.Column(db.String(200))
    views = db.Column(db.Integer,default = 0)
    created_id = db.Column(db.DateTime,default = datetime.utcnow)
    comments = db.relationship('ForumComment',backref = 'thread',lazy = True,cascade = 'all, delete-orphan')
    def to_dict(self):
        return {
            'id': self.id,
            'title':self.title,
            'content': self.content,
            'author': self.author.name if self.author else 'Unknown',
            'tags': self.tags.split(',') if self.tags else [],
            'views': self.views,
            'replies': len(self.comments),
            'timestamp': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'comments': [comment.to_dict() for comment in self.comments[:3]]
        }
class ForumComment(db.Model):
    __tablename__ = 'forum_comments'
    id = db.Column(db.Integer,primary_key = True)
    thread_id = db.Column(db.Integer,db.ForeignKey('forum_threads.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    content = db.Column(db.Text)
    created_id = db.Column(db.DateTime, default = datetime.utcnow)
    author = db.relationship('User','comments')
    def to_dict(self):
        return {
            'id': self.id,
            'author': self.author.name if self.author else 'Unknown',
            'content': self.content,
            'timestamp':self.created_at.strftime('%Y-%m-%d %H:%M')
        }
class Notification(db.Model):
    __tablename__ = 'notifications'
    id = db.Column(db.Integer,primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    type = db.Column(db.String(50))
    is_read = db.Column(db.Datetime,default = datetime.utcnow)
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'type': self.type,
            'is_read': self.is_read,
            'timestamp': self.created_at.strftime('%Y-%m-%d %H:%M')
        }