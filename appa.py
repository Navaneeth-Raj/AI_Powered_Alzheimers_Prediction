"""
from flask import Flask, request, redirect, render_template, session
from from_backend import *
app = Flask(__name__)
app.secret_key = '02ffcdcca96270df7c0cedfb28ac85f96e99aaec46b3d1fd2ce421e65c925604'

# Redirect the base URL to /login
@app.route('/')
def index():
    return redirect('/login')

# Route to serve the login form
@app.route('/login', methods=['GET'])
def login_display():
    return render_template('login.html')  

# Route to handle login form submission 
@app.route('/login', methods=['POST'])
def login_read():
    input_mail_id = request.form['username'] 
    input_password = request.form['password'] 
    connection = set_connection()
    user_check = None
    if connection: 
        user_check = login_details(connection, input_mail_id, input_password)
        cut_connection(connection)
        if user_check:
            session['user_id'] = user_check  
            return redirect('/todo')
        else:
            return "Login Failed.\nAre you Registered?"
    else:
        return "Connection Failed"

# Route to serve Register Form
@app.route('/signup')
def register():
    return render_template('signup.html')

# Route to handle signup form submission
@app.route('/signup', methods=['POST'])
def new_register():
    new_user = request.form['username']
    new_password = request.form['password']
    connection = set_connection()
    if connection:
        reg_check = reg_user(connection, new_user, new_password)
        cut_connection(connection)
        if reg_check:
            return render_template('reg_success.html', username=new_user)
        else: 
            return render_template('signup.html', error="Registration Failed. Please try again.")
    else:
        return render_template('signup.html', error="Failed Connecting to Database :(")
    
# Route to display saved tasks  
@app.route('/todo', methods=['GET'])
def task_get():
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    connection = set_connection()
    tasks = []
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT task_id, description FROM tasks WHERE user_id = %s", (user_id,))
            tasks = cursor.fetchall()
        finally:
            cursor.close()
            cut_connection(connection)
    return render_template('todo.html', tasks=tasks)

# Route to save tasks to SQL
@app.route('/todo', methods=['POST'])
def add_task():
    if 'user_id' not in session:
        return redirect('/login')    

    user_id = session['user_id']  
    data = request.get_json()  
    task_desc = data.get('description')
    if task_desc:
        connection = set_connection()
        if connection:
            try:
                cursor = connection.cursor()
                insert_query = "INSERT INTO tasks (user_id, description) VALUES (%s, %s)"
                cursor.execute(insert_query, (user_id, task_desc))
                connection.commit()
                task_id = cursor.lastrowid 
                return {"message": "Task added successfully", "task_id": task_id}, 201
            finally:
                cursor.close()
                cut_connection(connection)
    return {"message": "Failed to add task"}, 400

# Route to edit tasks
@app.route('/todo/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    if 'user_id' not in session:
        return redirect('/login')    

    user_id = session['user_id']
    data = request.get_json()
    task_desc = data.get('description')

    if task_desc:
        connection = set_connection()
        if connection:
            try:
                cursor = connection.cursor()
                update_query = "UPDATE tasks SET description = %s WHERE task_id = %s AND user_id = %s"
                cursor.execute(update_query, (task_desc, task_id, user_id))
                connection.commit()
                return {"message": "Task updated successfully"}, 200
            finally:
                cursor.close()
                cut_connection(connection)
    return {"message": "Failed to update task"}, 400

# Route to delete tasks
@app.route('/todo/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if 'user_id' not in session:
        return redirect('/login')

    user_id = session['user_id']
    
    connection = set_connection()
    if connection:
        try:
            cursor = connection.cursor()
            delete_query = "DELETE FROM tasks WHERE task_id = %s AND user_id = %s"
            cursor.execute(delete_query, (task_id, user_id))
            connection.commit()
            return {"message": "Task deleted successfully"}, 200
        finally:
            cursor.close()
            cut_connection(connection)
    
    return {"message": "Failed to delete task"}, 400

# Route for logging out
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
"""

