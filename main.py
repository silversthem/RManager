from flask import Flask, session, redirect, url_for, escape, request, render_template, send_from_directory
import sqlite3
from rmanager.User import User
from rmanager.Tasks import Tasks

# App configuration

app = Flask(__name__)
app.config['dbname'] = 'db.sqlite' # Database
app.secret_key = 'SECRETKEY' # secret key

# Static files

@app.route('/css/<path:path>') # css files access
def stylesheets(path):
    return send_from_directory('css',path)

@app.route('/js/<path:path>') # js files access
def scripts(path):
    return send_from_directory('js',path)

# Main App Views

# Index page
@app.route('/')
def main_page():
    return redirect(url_for('view_page',n=0)) # Equivalent to viewing page 0

# Page of tasks
# Search filters on tasks (teams, states, date, titles, descs)
@app.route('/page/<int:n>')
def view_page(n):
    db = sqlite3.connect(app.config['dbname'])
    user = User(session,db)
    if user.logged_on: # Connected user
        tasks = Tasks(user,db)
        # App menu and Task menu depending on rights
        app_menu = []
        task_menu = []
        # @TODO : Search filters and Pagination
        tasks_list = tasks.get_multiple(0,10,as_dict=True,with_steps=True)
        # Rendering
        db.close()
        return render_template('tasks.html',tasks=tasks_list,script='js/main.js')
    else: # Redirecting to login page
        db.close()
        return redirect(url_for('login'))

# Page of tasks for a specitic team
# Team dashboard
@app.route('/teams/<string:team>') # Team content
def view_team(team):
    return ''

# Steps search

# Task
# Task option : add, edit?id= , view?id= , delete?id=

# Handling data
@app.route('/task/<string:option>',methods=['POST'])
def task_scrud(option):
    db = sqlite3.connect(app.config['dbname'])
    user = User(session,db)
    tasks = Tasks(user,db)
    if user.logged_on:
        if option == 'new' and user.has_permission(5): # Adding task
            if tasks.add(request.form): # Adding Successful
            # @TODO : Error handling or confirmation
                return "Yeah"

# View
@app.route('/task/<string:option>')
def task_scrud_view(option):
    db = sqlite3.connect(app.config['dbname'])
    user = User(session,db)
    tasks = Tasks(user,db)
    if user.logged_on:
        if option == 'new' and user.has_permission(5): # Adding task
            task_data = Tasks.task()
            teams_available = user.get_all_teams() if user.has_permission(7) else User.get_teams()
            teams_available += [{'id':'all','name':'All'},{'id':'empty','name':''}]
            return render_template('task_form.html',script='js/task_form.js',edit=False,selected_teams=[],teams=teams_available,task=task_data)
        else: # Other options require id
            task_id = request.args.get('id')
            task_data = tasks.get(int(task_id))
            if task_data == None: # 404
                return 'Task not found'
            if option == 'edit' and user.has_permission(5): # Edits task
                # @TODO Get steps
                return render_template('task_form.html',script='js/task_form.js',edit=True,task=task_data)
            elif option == 'view': # Views task
                # @TODO Get steps
                return render_template('task_view.html',script='',task=task_data)
    return '404'

# Task Step SCRUD
# Step options : add, edit, view, change state, delete

# Handling Data
@app.route('/step/<int:task>/<int:step>',methods=['POST'])
def step_scrud():
    pass

# View
@app.route('/step/<int:task>/<int:step>')
def step_scrud_view():
    pass

# Privilege operations

# ...

# Analytic App Views

# ...

# Configuration

# ...

# User related

@app.route('/login',methods=['GET','POST']) # Login
def login():
    # User object
    db = sqlite3.connect(app.config['dbname'])
    user = User(session,db)
    # Form data if POST access
    username,pw = (request.form.get('username'),request.form.get('password'))
    if user.logged_on: # Already logged on
        db.close()
        return 'Logged on already !'
    elif username is None or pw is None: # GET access
        db.close()
        return render_template('login.html')
    else: # POST access
        if user.login(username,pw): # Successful login
            db.close()
            return redirect(url_for('main_page'))
        else:
            db.close()
            return 'Wrong login/password combination !'

@app.route('/logout') # Logout
def logout():
    db = sqlite3.connect(app.config['dbname'])
    user = User(session,db)
    if user.logged_on: # Disconnects user if logged on
        user.logout()
    db.close()
    return redirect('main_page') # Done
