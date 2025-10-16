import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib


df = pd.read_csv("data.csv")

# Fill missing values safely
df["Gender"] = df["Gender"].fillna("Male")
df["Married"] = df["Married"].fillna("Yes")
df["Dependents"] = df["Dependents"].fillna("0")
df["Self_Employed"] = df["Self_Employed"].fillna("No")
df["LoanAmount"] = df["LoanAmount"].fillna(df["LoanAmount"].mean())
df["Loan_Amount_Term"] = df["Loan_Amount_Term"].fillna(360)
df["Credit_History"] = df["Credit_History"].fillna(1.0)

# Encode categorical data
X = pd.get_dummies(df[["Gender", "Married", "ApplicantIncome", "CoapplicantIncome",
                       "LoanAmount", "Loan_Amount_Term", "Credit_History", "Property_Area"]],
                   drop_first=True)

y = df["Loan_Status"].map({"Y": 1, "N": 0})

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train model with more iterations
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# dumping into file for backend
joblib.dump(model, "loan_model.pkl")
joblib.dump(scaler, "scaler.pkl")


