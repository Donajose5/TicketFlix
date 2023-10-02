from database import db
from flask_security import UserMixin, RoleMixin
from datetime import datetime

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.user_id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.role_id'))) 

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    email = db.Column(db.String, unique = True, nullable = False)
    password = db.Column(db.String, nullable = False)
    name = db.Column(db.String, nullable = False)
    active = db.Column(db.Boolean())
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    roles = db.relationship('Role', secondary='roles_users',
                         backref=db.backref('users', lazy='dynamic'))
    @property
    def is_authorised(self):
    	return self.authenticated

class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    role_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False)
    description = db.Column(db.String(255), nullable = True)
    
class UserRole(db.Model):
    __tablename__ = 'userrole'
    user_role_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'), nullable = False)

class Venue(db.Model):
    __tablename__ = 'venue'
    venue_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, nullable = False, unique = True)
    location = db.Column(db.String, nullable = False)
    capacity = db.Column(db.Integer, nullable = False)
    
class Movie(db.Model):
    __tablename__ = 'movie'
    movie_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    name = db.Column(db.String, nullable = False)
    poster = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable = False)
    duration = db.Column(db.Integer, nullable = False)
    rating = db.Column(db.Float, nullable = True)
    tags = db.Column(db.String, nullable = True)

class Show(db.Model):
    __tablename__ = 'show'
    show_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.venue_id"), nullable = False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.movie_id'), nullable = False)
    datetime = db.Column(db.String, nullable = True)
    seats_available = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)

class Booking(db.Model):
    __tablename__ = 'booking'
    booking_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable = False)
    show_id = db.Column(db.Integer, db.ForeignKey('show.show_id'), nullable = False)
    datetime = db.Column(db.String, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    total_price = db.Column(db.Float, nullable = False)
    status = db.Column(db.String, nullable = False)
