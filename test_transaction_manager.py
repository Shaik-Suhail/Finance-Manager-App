import unittest
import sqlite3
from transaction_manager import (
    add_transaction,
    update_transaction,
    delete_transaction,
    check_budget,
    set_budget,
    connect_db,
)

class TestTransactionManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to the database and create tables for testing
        cls.conn = connect_db()
        cls.cursor = cls.conn.cursor()
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                type TEXT,
                amount REAL,
                category TEXT,
                date TEXT
            )
        """)
        cls.cursor.execute("""
            CREATE TABLE IF NOT EXISTS budgets (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                category TEXT,
                budget REAL
            )
        """)
        cls.conn.commit()
        
        # Add a sample transaction for testing
        cls.transaction_id = add_transaction(1, 'income', 1000, 'salary')

    @classmethod
    def tearDownClass(cls):
        cls.cursor.execute("DROP TABLE IF EXISTS transactions")
        cls.cursor.execute("DROP TABLE IF EXISTS budgets")
        cls.conn.commit()
        cls.conn.close()

    def test_add_transaction(self):
        transaction = add_transaction(1, 'expense', 200, 'groceries')
        self.assertIsNotNone(transaction)  # Ensure transaction was added successfully

    def test_update_transaction(self):
        # Assuming you have a method to update a transaction; you can reference the `transaction_id` added in setUpClass
        update_transaction()  # Add arguments based on your implementation
        transaction = self.cursor.execute("SELECT * FROM transactions WHERE id=?", (self.transaction_id,))
        self.assertIsNotNone(transaction.fetchone())  # Ensure the transaction exists after update

    def test_delete_transaction(self):
        delete_transaction()  # Add arguments based on your implementation
        transaction = self.cursor.execute("SELECT * FROM transactions WHERE id=?", (self.transaction_id,))
        self.assertIsNone(transaction.fetchone())  # Ensure transaction is deleted

    def test_set_budget(self):
        set_budget(1)  # Assuming this function works as intended
        self.cursor.execute("SELECT * FROM budgets WHERE user_id=?", (1,))
        budget = self.cursor.fetchone()
        self.assertIsNotNone(budget)  # Ensure budget was set

    def test_check_budget(self):
        set_budget(1)  # Ensure you set a budget first
        add_transaction(1, 'expense', 2000, 'salary')  # Exceed budget for testing
        result = check_budget(1)
        self.assertIn("exceeded your budget for salary", result)  # Check if alert is generated

if __name__ == '__main__':
    unittest.main()
