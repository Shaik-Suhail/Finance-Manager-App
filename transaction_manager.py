import sqlite3
import shutil
import os
from datetime import datetime

def connect_db():
    """Establish a connection to the SQLite database."""
    return sqlite3.connect('finance_manager.db')

def add_transaction(user_id, transaction_type, amount, category):
    """Add a new transaction to the database."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("INSERT INTO transactions (user_id, type, amount, category, date) VALUES (?, ?, ?, ?, ?)",
                       (user_id, transaction_type, amount, category, date))
        conn.commit()
        print("Transaction added successfully!")
        return cursor.lastrowid
    
    except Exception as e:
        print(f"Error adding transaction: {e}")
        return None
    
    finally:
        conn.close()

def update_transaction(transaction_id, transaction_type, amount, category):
    """Update an existing transaction in the database."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        # Check if the transaction exists
        cursor.execute("SELECT * FROM transactions WHERE id=?", (transaction_id,))
        transaction = cursor.fetchone()
        
        # Debugging: Print the found transaction (if any)
        print(f"Transaction before update: {transaction}")

        if not transaction:
            print("Transaction ID not found. Please try again.")
            return None  # Return None if the transaction ID doesn't exist
        
        # Update the transaction details
        cursor.execute("UPDATE transactions SET type=?, amount=?, category=? WHERE id=?",
                       (transaction_type, amount, category, transaction_id))
        conn.commit()
        print("Transaction updated successfully!")
    
    except Exception as e:
        print(f"Error updating transaction: {e}")
        return None
    
    finally:
        conn.close()


def delete_transaction(transaction_id):
    """Delete a transaction from the database."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM transactions WHERE id=?", (transaction_id,))
        transaction = cursor.fetchone()

        if not transaction:
            print("Transaction ID not found. Please try again.")
            return
        
        cursor.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
        conn.commit()
        print("Transaction deleted successfully!")
    
    except Exception as e:
        print(f"Error deleting transaction: {e}")
    
    finally:
        conn.close()

def list_transactions(user_id):
    """List all transactions for a specific user."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM transactions WHERE user_id=?", (user_id,))
        transactions = cursor.fetchall()
        
        if not transactions:
            print("No transactions found for this user.")
            return []
        
        print("\nTransactions:")
        for transaction in transactions:
            print(f"ID: {transaction[0]}, Type: {transaction[2]}, Amount: {transaction[3]}, "
                  f"Category: {transaction[4]}, Date: {transaction[5]}")
        return transactions
    
    except Exception as e:
        print(f"Error listing transactions: {e}")
        return None
    
    finally:
        conn.close()

def generate_monthly_report(user_id, month, year):
    """Generate a monthly financial report for a user."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT SUM(amount) FROM transactions 
        WHERE user_id=? AND type='income' AND strftime('%Y', date)=? AND strftime('%m', date)=?
    """, (user_id, year, month))
    total_income = cursor.fetchone()[0] or 0
    
    cursor.execute("""
        SELECT SUM(amount) FROM transactions 
        WHERE user_id=? AND type='expense' AND strftime('%Y', date)=? AND strftime('%m', date)=?
    """, (user_id, year, month))
    total_expenses = cursor.fetchone()[0] or 0
    
    savings = total_income - total_expenses
    print(f"\nMonthly Report for {month}/{year}:")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Savings: ${savings:.2f}")
    
    conn.close()

def generate_yearly_report(user_id, year):
    """Generate a yearly financial report for a user."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT SUM(amount) FROM transactions 
        WHERE user_id=? AND type='income' AND strftime('%Y', date)=?
    """, (user_id, year))
    total_income = cursor.fetchone()[0] or 0
    
    cursor.execute("""
        SELECT SUM(amount) FROM transactions 
        WHERE user_id=? AND type='expense' AND strftime('%Y', date)=?
    """, (user_id, year))
    total_expenses = cursor.fetchone()[0] or 0
    
    savings = total_income - total_expenses
    print(f"\nYearly Report for {year}:")
    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Savings: ${savings:.2f}")
    
    conn.close()

def set_budget(user_id, category, budget):
    """Set a budget for a specific category for a user."""
    conn = connect_db()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO budgets (user_id, category, budget) 
            VALUES (?, ?, ?) 
        """, (user_id, category, budget))
        
        conn.commit()
        print(f"Budget set for {category}: ${budget:.2f}")
    
    except Exception as e:
        print(f"Error setting budget: {e}")
    
    finally:
        conn.close()

def check_budget(user_id):
    """Check if the user's expenses exceed their set budgets."""
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM budgets WHERE user_id=?", (user_id,))
    budgets = cursor.fetchall()
    
    if not budgets:
        print("No budgets set. Please set a budget first.")
        return "No budgets set."
    
    budget_warnings = []
    print("\nBudget Check:")
    for budget in budgets:
        category = budget[2]
        budget_amount = budget[3]
        
        cursor.execute("""
            SELECT SUM(amount) FROM transactions 
            WHERE user_id=? AND category=? AND type='expense'
        """, (user_id, category))
        
        total_expense = cursor.fetchone()[0] or 0
        if total_expense > budget_amount:
            budget_warnings.append(f"Warning: You have exceeded your budget for {category}! "
                                   f"Budget: ${budget_amount:.2f}, Expenses: ${total_expense:.2f}")
        else:
            print(f"You are within budget for {category}. Budget: ${budget_amount:.2f}, "
                  f"Expenses: ${total_expense:.2f}")

    conn.close()

    return "\n".join(budget_warnings) if budget_warnings else "You are within your budget."

def backup_database():
    """Backup the SQLite database to a specified directory."""
    try:
        # Check if the 'backup/' directory exists, if not, create it
        if not os.path.exists('backup'):
            os.makedirs('backup')
        
        # Copy the database file to the backup directory
        shutil.copy('finance_manager.db', 'backup/finance_manager_backup.db')
        print("Database backup successful!")
    except Exception as e:
        print(f"Error backing up database: {e}")

def restore_database():
    """Restore the database from a backup."""
    try:
        # Check if the backup file exists
        if os.path.exists('backup/finance_manager_backup.db'):
            shutil.copy('backup/finance_manager_backup.db', 'finance_manager.db')
            print("Database restored successfully!")
        else:
            print("No backup found.")
    except Exception as e:
        print(f"Error restoring database: {e}")
