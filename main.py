from user_authentication import login, register  # Import login and registration functions
from transaction_manager import (                # Import transaction management functions
    add_transaction,
    update_transaction,
    delete_transaction,
    list_transactions,
    generate_monthly_report,  # Separate function for monthly reports
    generate_yearly_report,    # Separate function for yearly reports
    set_budget,
    check_budget,
    backup_database,
    restore_database
)

def main():
    while True:
        print("Welcome to Personal Finance Management Application")
        print("1. Register")
        print("2. Login")
        print("3. Backup Database")
        print("4. Restore Database")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            register()  # Call the register function
            print("Registration successful!")
        elif choice == '2':
            user_id = login()  # Call the login function and get user ID
            if user_id:  # Only proceed if login is successful
                while True:
                    print("\n1. Add Transaction")
                    print("2. Update Transaction")
                    print("3. Delete Transaction")
                    print("4. List Transactions")
                    print("5. Generate Monthly Report")
                    print("6. Generate Yearly Report")
                    print("7. Set Budget")
                    print("8. Check Budget")
                    print("9. Logout")
                    transaction_choice = input("Choose an option: ")

                    if transaction_choice == '1':
                        # Collect transaction details from the user
                        transaction_type = input("Enter transaction type (income/expense): ").strip().lower()
                        
                        # Validate transaction_type input
                        if transaction_type not in ['income', 'expense']:
                            print("Invalid transaction type. Please enter 'income' or 'expense'.")
                            continue  # Skip this iteration and go back to the transaction menu
                        
                        try:
                            amount = float(input("Enter the amount: "))  # Convert amount to float
                            if amount <= 0:
                                print("Amount must be a positive number.")
                                continue  # Skip this iteration and go back to the transaction menu
                        except ValueError:
                            print("Invalid input. Please enter a numeric value for amount.")
                            continue  # Skip this iteration and go back to the transaction menu
                        
                        category = input("Enter the category (e.g., Rent, Food): ")
                        
                        # Call the add_transaction function with the necessary arguments
                        add_transaction(user_id, transaction_type, amount, category)

                    elif transaction_choice == '2':
                        update_transaction()
                    elif transaction_choice == '3':
                        delete_transaction()
                    elif transaction_choice == '4':
                        transactions = list_transactions(user_id)
                        if transactions:
                            print("Transactions listed successfully.")
                    elif transaction_choice == '5':
                        try:
                            year = input("Enter year (YYYY): ")
                            month = input("Enter month (MM): ")
                            generate_monthly_report(user_id, year, month)
                        except Exception as e:
                            print(f"Error generating monthly report: {e}")
                    elif transaction_choice == '6':
                        try:
                            year = input("Enter year (YYYY): ")
                            generate_yearly_report(user_id, year)
                        except Exception as e:
                            print(f"Error generating yearly report: {e}")
                    elif transaction_choice == '7':
                        set_budget(user_id)
                    elif transaction_choice == '8':
                        check_budget(user_id)
                    elif transaction_choice == '9':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid option. Please try again.")

        elif choice == '3':
            backup_database()  # Call the backup function
        elif choice == '4':
            restore_database()  # Call the restore function
        elif choice == '5':
            print("Exiting the application.")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()  # Run the main function
