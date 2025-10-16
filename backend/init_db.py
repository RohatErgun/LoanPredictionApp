import sqlite3

# connecting sqlite database
# creates file if not exists
conn = sqlite3.connect("loan_predictions.db")
cursor = conn.cursor()

# predictions table create
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    gender TEXT,
    married TEXT,
    income REAL,
    coapplicant_income REAL,
    loan_amount REAL,
    loan_term REAL,
    credit_history REAL,
    property_area TEXT,
    result TEXT,
    probability REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
conn.close()
