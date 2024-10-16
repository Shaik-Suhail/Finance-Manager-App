import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('finance_manager.db')
cursor = conn.cursor()

# Create users table (if it doesn't exist)
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);
""")

# Create transactions table (if it doesn't exist)
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    type TEXT NOT NULL,  -- income or expense
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")

# Create budgets table (if it doesn't exist)
cursor.execute("""
CREATE TABLE IF NOT EXISTS budgets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    budget REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
""")

# Query to check existing tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Existing tables in the database:")
for table in tables:
    print(table[0])

# Commit changes and close the database connection
conn.commit()
conn.close()
