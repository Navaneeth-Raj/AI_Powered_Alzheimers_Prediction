import pickle
from flask import Flask, render_template, request
import pandas as pd
from sklearn.preprocessing import StandardScaler

# Load the model and scaler
with open("alzheimer_prediction_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("scaler.pkl", "rb") as scaler_file:
    scaler = pickle.load(scaler_file)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    import pandas as pd

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

    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
