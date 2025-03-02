from flask import Flask, request, redirect, render_template, session
import dbconnect
import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler 
with open("alzheimer_prediction_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)
with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)
app = Flask(__name__)

#index page routing
@app.route('/')
def show_index():
    return render_template('index.html')

#login page routing
@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    connection = dbconnect.set_connection()
    if connection:
        user_id = dbconnect.login_user(connection, username, password)
        if user_id:
            return redirect('/assess')
        else :
            return render_template('login.html', error='\nLogin Failed! Are You Registered?\n')
    else :
        return render_template('login.html', error='Connection Error! Contact Support')
            

#signup page routing
@app.route('/signup')
def show_signup():
    return render_template('signup.html')

@app.route('/signup', methods=["POST"])
def signup():
    form_dict = request.form.to_dict()
    connection = dbconnect.set_connection()
    if connection :
        success = dbconnect.signup_user(connection, form_dict)
        if success :
            return redirect('/login')
        else :
            return render_template('signup.html', error='\nSignup Failed! Contact Support\n')
    else:
        return render_template('signup.html', error='\nConnection Error')

#assess page routing
@app.route('/assess')
def show_assess():
    return render_template('assess.html')