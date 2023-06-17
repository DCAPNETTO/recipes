from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


class User:
    db = "recipes"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

#CREATE USERS MODEL
    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO users (first_name, last_name, email, created_at, updated_at) 
        VALUES (%(first_name)s, %(last_name)s, %(email)s, NOW(), NOW())
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def register_user(cls, user_info):
        if not cls.validate_user_data(user_info):
            return False
        user_info = cls.parse_user_data(user_info)
        query = """
        INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())
        ;"""
        user_id = connectToMySQL(cls.db).query_db(query, user_info)
        session['user_id'] = user_id
        session['user_name'] = f'{user_info["first_name"]} {user_info["last_name"]}'
        return user_id



#READ USERS MODEL
    @classmethod
    def get_all_users(cls):
        query = """
        SELECT * 
        FROM users
        ;"""
        results = connectToMySQL(cls.db).query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

    @classmethod
    def get_user_by_id(cls, id):
        query  = """
        SELECT * 
        FROM users 
        WHERE id = %(id)s
        ;"""
        data = {'id': id}
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = """
        SELECT * 
        FROM users
        WHERE email = %(email)s
        ;"""
        user_data = connectToMySQL(cls.db).query_db(query, data)
        if user_data:
            return cls(user_data[0])
        return False

    @classmethod
    def get_user_with_recipes(cls, user_id):
        query = """
        SELECT *
        FROM users
        LEFT JOIN recipes ON recipes.user_id = users.id
        WHERE users.id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, {'id' : user_id})
        user = cls(result[0])
        for recipe in result:
            recipe_data = {
                "user_id" :recipe['user_id'],
                "name" : recipe['name'],
                "description" : recipe['description'],
                "instructions" : recipe['instructions'],
                "date_made" : recipe['date_made'],
                "under_30_minutes" : recipe['under_30_minutes'],
                "created_at" : recipe['created_at'],
                "updated_at" : recipe['updated_at'],
            }
            user.recipes.append(recipe_data)
        return user


#UPDATE
    @classmethod
    def update_user(cls, user_data):
        if not cls.validate_user_data(user_data):
            return False
        query = """
        UPDATE users
        SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, user_data)
        return True

    @classmethod
    def update(cls, data):
        query = """
        UPDATE users 
        SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s 
        WHERE id = %(id)s
        ;"""
        result= connectToMySQL(cls.DB).query_db(query, data)
        return result

#DELETE
    @classmethod
    def delete(cls, id):
        query  = """
        DELETE FROM users 
        WHERE id = %(id)s
        ;"""
        data = {"id": id}
        # print(data)
        result = connectToMySQL(cls.DB).query_db(query, data)    
        return result

    # Login / Logout Models
    @staticmethod
    def login(data):
        this_user = User.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password , data['password']):
                session['user_id'] = this_user.id
                session['user_name'] = f'{this_user.first_name} {this_user.last_name}'
                return True
        flash("Your Login Password or Email is incorrect.")
        return False   


    #```````USER'S CRUD as Follows`````````#
    
    #USER READ POSTS
    @classmethod
    def user_show_posts_to_wall(cls, user_id):
        query = """
            SELECT *
            FROM users
            LEFT JOIN posts ON posts.user_id = users.id 
            WHERE users.id = %(id)s
            ;"""
        results = connectToMySQL(cls.db).query_db(query, {'id' : user_id})
        user = cls(result[0])
        for recipe in result:
            recipe_data = {
                "user_id" :recipe['user_id'],
                "name" : recipe['name'],
                "description" : recipe['description'],
                "instructions" : recipe['instructions'],
                "date_made" : recipe['date_made'],
                "under_30_minutes" : recipe['under_30_minutes'],
                "created_at" : recipe['created_at'],
                "updated_at" : recipe['updated_at'],
            }
            user.recipes.append(recipe_data)
        return user


    # HELPER FUNCTIONS in Models
    @staticmethod
    def validate_user_data(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # PASSWORD_REGEX = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$')
        is_valid = True
        if 'id' not in data:
            if len(data['first_name']) < 2 :
                flash("First Name must be at least 2 characters.")
                is_valid = False
            if len(data['last_name']) < 2 :
                flash("Last Name must be at least 2 characters.")
                is_valid = False  
            # if not PASSWORD_REGEX.match(data['password']):
            #     flash("Password must be minimum eight characters, at least one uppercase letter, one lowercase letter and one number.")
            #     is_valid = False
            if data['password'] != data['confirm_password'] :
                flash("Passwords do not match.")
        if 'id' not in data or data['email'] != User.get_user_by_id(data['id']).email :
            if not EMAIL_REGEX.match(data['email']) :
                flash("Please use valid email address")
                is_valid = False
                is_valid = False
            if User.get_user_by_email(data['email']) :
                flash("Email is taken")
                is_valid = False
        return is_valid

    @staticmethod    
    def parse_user_data(data):
        parsed_data = {
            'email' : data['email'],
            'first_name' : data['first_name'],
            'last_name' : data['last_name'],
            'password' : bcrypt.generate_password_hash(data['password'])
        }
        return(parsed_data)