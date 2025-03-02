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

@app.route('/') 
def land():
    return(redirect('/login'))

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    user_name = request.form['username']
    pass_word = request.form['password']
    connection = dbconnect.set_connection()
    if connection :
        user_id = dbconnect.login_details(connection, user_name, pass_word)
        dbconnect.cut_connection(connection)
        print(user_id)
        if user_id :
            #session['user_id'] = user_id
            return redirect('/index')
        else :
            return render_template('login.html', error='\nLogin Failed! Are You Registered?\n')
    else :
        return render_template('login.html', error='Connection Error! Contact Support')

@app.route('/signup')
def sign_page():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    user_name = request.form['username']
    pass_word = request.form['password']
    connection = dbconnect.set_connection()
    if connection :
        success = dbconnect.register_user(connection, user_name, pass_word) 
        dbconnect.cut_connection(connection)
        if success :
            return render_template('register_success.html', username=user_name)
        else :
            return render_template('signup.html', error='Registration Error! Contact Support')
    else :
        return render_template('signup.html', error='Connection Error! Contact Support')
    
@app.route('/index')
def main_page():    
    return render_template('index.html')

@app.route('/index',methods=['POST'])
def predict():
    # Extract user input from the form
    features = request.form.to_dict()

    # Create a DataFrame with features in the same order as training data
    X_new = pd.DataFrame([features], columns=['MMSE', 'FunctionalAssessment', 'MemoryComplaints', 'BehavioralProblems', 'ADL']) 

    # Scale the features
    X_new_scaled = scaler.transform(X_new) 

    # Make predictions
    prediction = model.predict(X_new_scaled)[0] 
    probability = model.predict_proba(X_new_scaled)[0][1] 

    # Prepare the prediction result for the template
    result = {
        "prediction": prediction,
        "probability": probability
    }
    
    return render_template('result.html',result=result)

@app.route('/register_success')
def display_register():
    return render_template('register_success.html')
    
if __name__ == '__main__' :
    app.run(debug=True)