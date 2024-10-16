import sqlite3
import bcrypt

# Function to register a new user
def register():
    # Connect to the SQLite database
    conn = sqlite3.connect('finance_manager.db')
    cursor = conn.cursor()
    
    # Prompt the user for a username and password
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Check if the username already exists in the database
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    if cursor.fetchone():
        print("Username already exists. Please choose a different username.")
        conn.close()
        return
    
    # Hash the password using bcrypt
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    
    # Insert the username and hashed password into the users table
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_pw))
    
    # Commit the changes and close the database connection
    conn.commit()
    conn.close()
    
    print("User registered successfully!")

# Run the register function
register()
