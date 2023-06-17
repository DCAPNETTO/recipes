from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, recipe # import entire file, rather than class, to avoid circular imports

# Create Users Controller

@app.route('/users/register', methods=['POST'])
def register_user():
    if user.User.register_user(request.form):
        return redirect('/recipes/all')
    return redirect('/')


# Read Users Controller

@app.route('/')
def index():
    return render_template('login_and_register.html')

@app.route('/users/all')
def show_all_users():
    if 'user_id' not in session: return redirect('/')
    all_users = user.User.get_all_users()
    return render_template('show_all_users.html', users = all_users)

@app.route('/users/<int:user_id>/profile')
def show_user_by_id(user_id):
    user= User.get_user_by_id(user_id)
    return render_template("show_user.html", user = user)


# Update Users Controller

@app.route('/users/<int:id>/update', methods=['GET','POST'])
def update_user(id):
    if request.method == 'GET':
        this_user = user.User.get_user_by_id(id)
        return render_template('edit_profile.html' , user = this_user)
    if user.User.update_user(request.form):
        return redirect('/users/all')
    return redirect(f'/users/{id}/profile')

# Delete Users Controller

@app.route('/users/delete/<int:user_id>')
def delete_user(user_id):
    User.delete(user_id)
    return redirect('/')

# LOGIN / LOGOUT Controllers 

@app.route('/users/login', methods=['POST'])
def login_user():
    if user.User.login(request.form):
        return redirect('/recipes/all')
    return redirect('/')

@app.route('/users/logout')
def logout():
    session.clear()
    return redirect('/')    

# USER'S WALL CONTROLLER
@app.route('/users/<int:user_id>/wall')
def user_wall(user_id):
    this_user = user.User.get_user_by_id(user_id)
    all_posts = user.User.user_show_posts_to_wall(user_id)
    return render_template('user_wall.html', user = user.User.get_user_with_posts(user_id), posts = all_posts)

# Notes:
# 1 - Use meaningful names
# 2 - Do not overwrite function names
# 3 - No matchy, no worky
# 4 - Use consistent naming conventions 
# 5 - Keep it clean
# 6 - Test every little line before progressing
# 7 - READ ERROR MESSAGES!!!!!!
# 8 - Error messages are found in the browser and terminal




# How to use path variables:
# @app.route('/<int:id>')
# def index(id):
#     user_info = user.User.get_user_by_id(id)
#     return render_template('index.html', user_info)

# Converter -	Description
# string -	Accepts any text without a slash (the default).
# int -	Accepts integers.
# float -	Like int but for floating point values.
# path 	-Like string but accepts slashes.
