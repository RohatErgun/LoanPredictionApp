from flask import Flask, request, jsonify
import joblib
import numpy as np
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model and scaler
model = joblib.load("../model/loan_model.pkl")
scaler = joblib.load("../model/scaler.pkl")

DB_FILE = "loan_predictions.db"

def save_prediction(data, result, probability):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO predictions 
        (gender, married, income, coapplicant_income, loan_amount, loan_term, 
         credit_history, property_area, result, probability) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["gender"],
        data["married"],
        float(data["income"]),
        float(data["coapplicant_income"]),
        float(data["loan_amount"]),
        float(data["loan_term"]),
        float(data["credit_history"]),
        data["property_area"],
        result,
        round(probability * 100, 2)
    ))
    conn.commit()
    conn.close()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # Encode categorical features
    gender_male = 1 if data.get("gender") == "Male" else 0
    married_yes = 1 if data.get("married") == "Yes" else 0
    property_urban = 1 if data.get("property_area") == "Urban" else 0
    property_semiurban = 1 if data.get("property_area") == "Semiurban" else 0

    X = np.array([[
        float(data.get("income")),
        float(data.get("coapplicant_income")),
        float(data.get("loan_amount")),
        float(data.get("loan_term", 360)),
        float(data.get("credit_history", 1)),
        gender_male,
        married_yes,
        property_urban,
        property_semiurban
    ]])

    # Scale input
    X_scaled = scaler.transform(X)

    # Predict
    prediction = model.predict(X_scaled)[0]
    probability = model.predict_proba(X_scaled)[0][1]
    result = "Loan Approved" if prediction == 1 else "Loan Rejected"

    # Save prediction in SQLite
    save_prediction(data, result, probability)

    return jsonify({
        "result": result,
        "approval_probability": round(probability * 100, 2)
    })

if __name__ == "__main__":
    app.run(debug=True)
