import unittest
from transaction_manager import (
    add_transaction,
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
        print(f"Transaction ID for testing: {cls.transaction_id}")  # Debugging: Print transaction ID

    @classmethod
    def tearDownClass(cls):
        # Cleanup: Drop the test tables and close the connection
        cls.cursor.execute("DROP TABLE IF EXISTS transactions")
        cls.cursor.execute("DROP TABLE IF EXISTS budgets")
        cls.conn.commit()
        cls.conn.close()

    def setUp(self):
        # Ensure a fresh state before each test
        self.conn = connect_db()
        self.cursor = self.conn.cursor()

    def tearDown(self):
        # Close the connection after each test
        self.conn.close()

    def test_add_transaction(self):
        # Test adding a new transaction
        transaction_id = add_transaction(1, 'expense', 200, 'groceries')
        self.assertIsNotNone(transaction_id)  # Ensure transaction was added successfully

        # Verify transaction in the database
        transaction = self.cursor.execute("SELECT * FROM transactions WHERE id=?", (transaction_id,))
        self.assertIsNotNone(transaction.fetchone())  # Check if the transaction exists

    @unittest.skip("Skipping update transaction test for now")
    def test_update_transaction(self):
        # This test will be skipped
        pass  # Optional: Placeholder if needed

    def test_delete_transaction(self):
        # Delete the transaction
        delete_transaction(self.transaction_id)
        
        # Verify transaction was deleted
        transaction = self.cursor.execute("SELECT * FROM transactions WHERE id=?", (self.transaction_id,))
        self.assertIsNone(transaction.fetchone())  # Ensure the transaction is deleted

    def test_set_budget(self):
        # Set a budget for a category
        set_budget(1, 'groceries', 500)
        
        # Verify the budget is set in the database
        budget = self.cursor.execute("SELECT * FROM budgets WHERE user_id=? AND category=?", (1, 'groceries'))
        self.assertIsNotNone(budget.fetchone())  # Ensure the budget was set

    def test_check_budget(self):
        # Set a budget and add a transaction exceeding that budget
        set_budget(1, 'salary', 1000)
        add_transaction(1, 'expense', 2000, 'salary')  # Exceed the budget
        
        # Check if budget warning is generated
        result = check_budget(1)
        self.assertIn("exceeded your budget for salary", result)  # Verify warning message

if __name__ == '__main__':
    unittest.main()
