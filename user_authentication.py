# user_authentication.py

import sqlite3
import bcrypt

def connect_db():
    return sqlite3.connect('finance_manager.db')

def register():
    conn = connect_db()
    cursor = conn.cursor()
    
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        print("Username already exists.")
        conn.close()
        return
    
    # Hash the password
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    # Insert into database
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
    conn.commit()
    conn.close()
    print("User registered successfully!")

def login():
    conn = connect_db()
    cursor = conn.cursor()
    
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    cursor.execute("SELECT id, password FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    conn.close()
    
    if user and bcrypt.checkpw(password.encode(), user[1]):  # user[1] should be the hashed password
        print("Login successful!")
        return user[0]  # Return the user ID
    else:
        print("Invalid username or password.")
        return None  # Return None if login fails