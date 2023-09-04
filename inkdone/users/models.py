from inkdone import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    bio = db.Column(db.String(1000), unique=False, nullable=True, default="No bio is set by the user...")
    password = db.Column(db.String(300), nullable=False, unique=False)
    image = db.Column(db.String(20), nullable=True, unique=False)
    academics = db.Column(db.String(1500), unique=False, nullable=True, default="No academic details is set by the user...")
    accomplishment = db.relationship('Accomplishment', backref='user', cascade='all, delete, delete-orphan')

    def __repr__(self):
        return self.username
    
    def check_password(self, form_password):
        return bcrypt.check_password_hash(self.password, form_password)
        
    @property
    def password_hash(self):
        return self.password
    
    @password_hash.setter
    def password_hash(self, plain_password):
        self.password = bcrypt.generate_password_hash(plain_password).decode('utf-8')
    

class Accomplishment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'), unique=True)
    name = db.Column(db.String(50), unique=False, nullable=False)
    description = db.Column(db.String(3000), unique=False, nullable=False)

    def __repr__(self):
        return self.name