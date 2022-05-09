from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask_app import app
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class User:
    db = 'burbankauto'

    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_user(cls, data):
        if cls.validate_user(data):
            data = cls.parse_user_data(data)
        else:
            return False
        query = """
        INSERT INTO users (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)
        ;"""
        user_id = MySQLConnection(cls.db).query_db(query, data)
        print(user_id)
        session['user_id'] = user_id
        return user_id

    @classmethod
    def get_user_by_email(cls, email):
        data = { 'email' : email }
        query = """
        SELECT * 
        FROM users
        WHERE email = %(email)s
        ;"""
        result = MySQLConnection(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result

    @classmethod
    def login_user(cls, data):
        user = cls.get_user_by_email(data['email'])
        if user:
            if bcrypt.check_password_hash(user.password, data['password']):
                session['user_id'] = user.id
                session['first_name'] = user.first_name
                return True
        flash('Login info incorrect.', 'login')
        return False

    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters.', 'register')
            is_valid = False
        if len(data['last_name']) < 2 :
            flash('Last name must be at least 2 characters.', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Please use a valid email.', 'register')
            is_valid = False
        if User.get_user_by_email(data['email']):
            flash('Email is already in use.', 'register')
            is_valid = False
        if len(data['password']) < 8 or data['password'].isalpha() or data['password'].islower():
            flash('Your password must contain at least eight characters, at least 1 upper case, and one number.', 'register')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Passwords must match.', 'register')
            is_valid = False
        print(is_valid)
        return is_valid

    @staticmethod
    def parse_user_data(data):
        parsed_data = {
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'email' : data['email'],
            'password' : bcrypt.generate_password_hash(data['password'])
        }
        return parsed_data