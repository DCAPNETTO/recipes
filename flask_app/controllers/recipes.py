from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, recipe 
from flask_app.controllers import users

#CREATE RECIPES

@app.route('/recipes/create', methods=['GET','POST'])
def create_recipe():
    if request.method == 'GET':
        return render_template('create_recipe.html')
    if recipe.Recipe.create_recipe(request.form):
        return redirect('/recipes/all')
    return redirect('/recipes/create')

#READ RECIPES

@app.route('/recipes/all')
def show_all_user_recipes():
    if 'user_id' not in session: return redirect('/')
    all_recipes = recipe.Recipe.show_all_user_recipes()
    print(session)
    # print(all_recipes) 
    return render_template('/show_all_recipes.html', recipes=all_recipes, user = user)

@app.route('/recipes/<int:id>/view')
def show_recipe_by_id(id):
    this_recipe = recipe.Recipe.get_recipe_by_id(id)
    # print("############", this_recipe)
    return render_template('show_recipe_by_id.html', recipe = this_recipe)



#UPDATE RECIPES

@app.route('/recipes/<int:id>/update', methods=['GET','POST'])
def update_recipe(id):
    if 'user_id' not in session: return redirect('/')
    if 'user_id' == session['user_id']:
        if request.method == 'GET':
            this_recipe = recipe.Recipe.get_recipe_by_id(id)
            return render_template('edit_recipe.html' , recipe = this_recipe)
        if recipe.Recipe.update_recipe(request.form):
                print("update should have worked.")
                return redirect('/recipes/all')
    return redirect(f'/recipes/{id}/view')


#DELETE RECIPES
@app.route('/recipes/<int:id>/delete')
def delete_recipe(id):
    recipe.Recipe.delete_recipe(id)
    return redirect('/recipes/all')

