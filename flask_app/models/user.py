from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import app
import re 
from flask import flash
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "login_and_registration_schema"
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.birthday = data['birthday']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, birthday, email, password) VALUES (%(first_name)s, %(last_name)s, %(birthday)s, %(email)s, %(password)s);"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False

        return cls(results[0])

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM users where id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results


    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(User.db).query_db(query, user)

        if len(user['first_name']) < 2 or len(user['last_name']) < 2 :
            flash("Name must be 3 Characters.")
            is_valid = False 
        
        if user['first_name'].isalpha() == False or user['last_name'].isalpha() == False:
            flash("Name must consist of only Letters.")
            is_valid = False

        if len(user['birthday']) < 1:
            flash("Birthday required.")
            is_valid = False

        if len(results) >= 1:
            flash("Email in use. Try again")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid Email Address.")
            is_valid = False

        if len(user['password']) < 8 :
            flash("Password must be 8 Characters.")
            is_valid = False
        
        if user['password'].isalpha() == True :
            flash("Password must contain at least 1 Number.")
            is_valid = False

        if user['password'].islower() == True :
            flash("Password must contain 1 Uppercase Letter.")
            is_valid = False

        if user['password'] != user['password_confirm']:
            flash("Passwords do not match.")
            is_valid = False

        return is_valid

