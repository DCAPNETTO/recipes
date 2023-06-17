
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models import user
import re


class Recipe:
    db = "recipes"
    def __init__(self,data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under_30_minutes = data['under_30_minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

#CREATE RECIPE 

    @classmethod
    def create_recipe(cls, recipe_info):
        # print("*=*=*=*=*=*=*=*=*=*=*=*", data)
        if not cls.validate_recipe_data(recipe_info):
            return False
        recipe_info = cls.parse_recipe_data(recipe_info)
        query = """
        INSERT INTO recipes (user_id, name, description, instructions, date_made, under_30_minutes)
        VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under_30_minutes)s)
        ;"""
        recipe_id = connectToMySQL(cls.db).query_db(query, recipe_info)
        # print(recipe_id)
        return recipe_id

# READ RECIPE

    @classmethod
    def show_all_user_recipes(cls):
        query = """
            SELECT *
            FROM recipes
            JOIN users ON recipes.user_id = users.id 
            ;"""
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for row in results:
            posting_user = {
                "id": row["user_id"],
                "email": row["email"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "password": row["password"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }
            new_recipe_data = {
                "id" :row['id'],
                "name" : row['name'],
                "description" : row['description'],
                "instructions" : row['instructions'],
                "date_made" : row['date_made'],
                "under_30_minutes" : row['under_30_minutes'],
                "created_at" : row['created_at'],
                "updated_at" : row['updated_at'],
                "user": posting_user
            }
            all_recipes.append(new_recipe_data)
        return all_recipes

    @classmethod
    def get_recipe_by_id(cls, id):
        query = """
        SELECT *
        FROM recipes
        JOIN users 
        ON recipes.user_id = users.id
        WHERE recipes.id = %(id)s
        ;"""
        data = {'id' : id}
        results = connectToMySQL(cls.db).query_db(query, data)
        # print(results)
        recipe_creator = {
            "id" : results[0]['id'],
            "first_name" : results[0]["first_name"],
            "last_name" : results[0]['last_name'],
            "email" : results[0]['email'],
            "password" : results[0]['password'],
            "created_at" : results[0]['created_at'],
            "updated_at" : results[0]['updated_at'],
            "user_id" : results[0]['user_id'], 
            "name" : results[0]['name'],
            "description" : results[0]['description'],
            "instructions" : results[0]['instructions'],
            "date_made" : results[0]['date_made'],
            "under_30_minutes" : results[0]['under_30_minutes']
        }
        print("*************", recipe_creator)
        return recipe_creator


# UPDATE RECIPE

    @classmethod
    def update_recipe(cls, recipe_data):
        print("*=*=*=*=*=*", "Updating recipe...", "*=*=*=*=*=*" )
        if not cls.validate_recipe_data(recipe_data):
            return False
        query = """
        UPDATE recipes
        SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made=%(date_made)s, under_30_minutes=%(under_30_minutes)s
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, recipe_data)
        print("Recipe updated successfully")
        print(result)
        return True

# DELETE RECIPE

    @classmethod
    def delete_recipe(cls, id):
        data = {"id" : id}
        query = """
        DELETE FROM recipes 
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        return result

#HELPER FUNCTIONS

#''' 6/15/23 NOT ABLE TO GET UPDATE METHOD TO WORK CORRECTLY .. 
#I THINK IT HAS TO DO WITH MY VALIDATION FEATURE AT THE UNDER 30 MINUTES'''


    @staticmethod
    def validate_recipe_data(data):
        is_valid= True
        if 'id' not in data:
            if len(data['description']) <= 2:
                flash("Post must contain description.")
                is_valid = False
            if len(data['instructions']) <= 2:
                flash("Post must contain instructions.")
                is_valid = False
            if len(data['date_made']) == 0:
                flash("Post must contain date that it was made.")
                is_valid = False
            if 'under_30_minutes' not in data:
                flash("Please mark if recipe takes less than 30 minutes.")
                is_valid = False
        print("Validation result is:", is_valid)        
        return is_valid

    @staticmethod    
    def parse_recipe_data(data):
        parsed_data = {
            'user_id' : data['user_id'],
            'name' : data['name'],
            'description' : data['description'],
            'instructions' : data['instructions'],
            'date_made' : data['date_made'],
            'under_30_minutes' : data['under_30_minutes']
        }
        return(parsed_data)