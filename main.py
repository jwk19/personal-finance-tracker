from models import User, Category, Transaction
from db import get_connection  # Assuming this is in db.py

def print_menu():
    """Print the options menu."""
    print("\nPersonal Finance Tracker")
    print("1. Add User")
    print("2. Add Category")
    print("3. Add Transaction")
    print("4. Retrieve Transaction by ID")
    print("5. Delete Transaction by ID")
    print("6. View All Users")
    print("7. View All Categories")
    print("8. View All Transactions")
    print("9. Exit")

def add_user():
    """Add a new user interactively."""
    name = input("Enter the user's name: ")
    user = User(name=name)
    user.save()
    print(f"User {user.name} added with ID {user.user_id}")

def add_category():
    """Add a new category interactively after getting the user ID."""
    user_id = int(input("Enter the user ID to associate the category with: "))
    
    # Check if the category already exists; if not, add it
    category_name = input("Enter the category name: ")
    
    # Check if category exists
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM categories WHERE name = %s;", (category_name,))
    category = cur.fetchone()
    
    if category:
        print(f"Category '{category_name}' already exists with ID {category[0]}")
        category_id = category[0]
    else:
        # If category does not exist, add it
        cur.execute("INSERT INTO categories (name) VALUES (%s) RETURNING id;", (category_name,))
        category_id = cur.fetchone()[0]
        conn.commit()
        print(f"Category '{category_name}' added with ID {category_id}")
    
    cur.close()
    conn.close()

def add_transaction():
    """Add a new transaction interactively."""
    user_name = input("Enter the user's name: ")
    
    # Get the user ID based on the user's name
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE name = %s;", (user_name,))
    user = cur.fetchone()
    
    if user:
        user_id = user[0]
        print(f"User '{user_name}' found with ID {user_id}")
    else:
        print(f"User '{user_name}' not found.")
        cur.close()
        conn.close()
        return

    # Display available categories for the user to choose from
    cur.execute("SELECT id, name FROM categories;")
    categories = cur.fetchall()
    
    if categories:
        print("\nAvailable Categories:")
        for category in categories:
            print(f"ID: {category[0]}, Name: {category[1]}")
        category_id = int(input("\nEnter the Category ID from the above list: "))
    else:
        # If no categories exist, prompt to add one
        print("No categories found. Please add a category first.")
        cur.close()
        conn.close()
        return

    # Ask for transaction details
    amount = float(input("Enter the transaction amount: "))
    type = input("Enter the transaction type (income/expense): ").lower()
    description = input("Enter a description for the transaction: ")

    # Allow users to input an optional date (default to current date if left empty)
    date = input("Enter the date for the transaction (YYYY-MM-DD) or leave blank for today's date: ")
    if date.strip() == "":
        date = None
    
    # Save the transaction
    transaction = Transaction(user_id=user_id, category_id=category_id, amount=amount, type=type, description=description, date=date)
    transaction.save()
    print(f"Transaction added with ID {transaction.transaction_id}")

    cur.close()
    conn.close()

def retrieve_transaction():
    """Retrieve and display a transaction by ID."""
    transaction_id = int(input("Enter the transaction ID to retrieve: "))
    transaction = Transaction.get(transaction_id)
    if transaction:
        print(f"Transaction {transaction.transaction_id}: User {transaction.user_id}, Category {transaction.category_id}, Amount {transaction.amount}, Type {transaction.type}, Date {transaction.date}, Description: {transaction.description}")
    else:
        print(f"No transaction found with ID {transaction_id}")

def delete_transaction():
    """Delete a transaction by ID."""
    transaction_id = int(input("Enter the transaction ID to delete: "))
    Transaction.delete(transaction_id)
    print(f"Transaction {transaction_id} deleted successfully.")

def view_users():
    """View all existing users."""
    print("\nExisting Users:")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users;")
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}")
    else:
        print("No users found.")
    cur.close()
    conn.close()

def view_categories():
    """View all existing categories."""
    print("\nExisting Categories:")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM categories;")
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Category: {row[1]}")
    else:
        print("No categories found.")
    cur.close()
    conn.close()

def view_transactions():
    """View all existing transactions."""
    print("\nExisting Transactions:")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.id, u.name, c.name, t.amount, t.type, t.date, t.description 
        FROM transactions t
        JOIN users u ON t.user_id = u.id
        JOIN categories c ON t.category_id = c.id;
    """)
    rows = cur.fetchall()
    if rows:
        for row in rows:
            print(f"Transaction ID: {row[0]}, User: {row[1]}, Category: {row[2]}, Amount: {row[3]}, Type: {row[4]}, Date: {row[5]}, Description: {row[6]}")
    else:
        print("No transactions found.")
    cur.close()
    conn.close()

def main():
    """Main function to run the menu."""
    while True:
        print_menu()
        choice = input("\nSelect an option (1-9): ")

        if choice == "1":
            add_user()
        elif choice == "2":
            add_category()
        elif choice == "3":
            add_transaction()
        elif choice == "4":
            retrieve_transaction()
        elif choice == "5":
            delete_transaction()
        elif choice == "6":
            view_users()
        elif choice == "7":
            view_categories()
        elif choice == "8":
            view_transactions()
        elif choice == "9":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid option. Please choose a number between 1 and 9.")

if __name__ == "__main__":
    main()
