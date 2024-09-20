---

# Personal Finance Tracker

## Overview
The **Personal Finance Tracker** is a command-line tool that helps users manage their personal finances, categorize their transactions, and keep track of income, expenses, and savings. It provides an easy-to-use interface for adding, viewing, and deleting transactions while categorizing them for better financial management.

This project uses a **PostgreSQL** database to store user data, categories, and transactions. The tool is designed to be used offline and provides functionality via a simple menu-driven interface.

## Features
- **Add Users**: Users can be added to track personal transactions.
- **Add Categories**: Categories (like "Groceries", "Rent", etc.) can be added to categorize transactions. 
- **Add Transactions**: Transactions (income or expense) can be added with descriptions, amounts, and associated categories.
- **View Data**: Users can view all users, categories, and transactions from the command-line interface.
- **Delete Transactions**: Individual transactions can be deleted by ID.
- **View Summaries**: Lists of users, categories, and transactions can be viewed for easier management.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Menu Options](#menu-options)
- [Database Setup](#database-setup)
- [Contribution](#contribution)

## Installation

### 1. Clone the repository:
```bash
git clone git@github.com:jwk19/personal-finance-tracker.git
cd personal-finance-tracker
```

### 2. Create and activate a virtual environment:
Using `pipenv` (recommended):
```bash
pipenv install
pipenv shell
```

Alternatively, using `virtualenv` and `pip`:
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
```

### 3. Install PostgreSQL:
Make sure you have **PostgreSQL** installed on your system. Follow the appropriate installation instructions for your OS:
- macOS: `brew install postgresql`
- Linux: `sudo apt install postgresql`
- Windows: [Download from here](https://www.postgresql.org/download/)

### 4. Configure the database connection:
Update the `db.py` file with your PostgreSQL database credentials:
```python
DB_NAME = "your_database_name"
DB_USER = "your_database_user"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
```

### 5. Set up the database:
Run the following command to create the necessary tables:
```bash
python db.py
```

## Usage

To start the program, run:

```bash
python main.py
```

This will start a menu-driven interface that allows you to interact with the Personal Finance Tracker.

## Menu Options

When you run the program, you will be presented with the following menu:

```
Personal Finance Tracker
1. Add User
2. Add Category
3. Add Transaction
4. Retrieve Transaction by ID
5. Delete Transaction by ID
6. View All Users
7. View All Categories
8. View All Transactions
9. Exit
```

### 1. **Add User**: 
- Prompts the user to enter a name, which will be saved in the database.

### 2. **Add Category**: 
- Prompts for a user ID and category name. If the category does not already exist, it is added to the database.

### 3. **Add Transaction**: 
- Prompts the user to enter a name to match the user ID. 
- Displays all categories and allows the user to select one by ID.
- Allows the user to enter transaction details, including amount, type (income/expense), and description.

### 4. **Retrieve Transaction by ID**: 
- Prompts for a transaction ID and retrieves the associated transaction details.

### 5. **Delete Transaction by ID**: 
- Prompts for a transaction ID and deletes the transaction.

### 6. **View All Users**: 
- Displays a list of all users with their IDs and names.

### 7. **View All Categories**: 
- Displays a list of all categories with their IDs and names.

### 8. **View All Transactions**: 
- Displays a list of all transactions, including transaction ID, user name, category name, amount, type (income/expense), and description.

### 9. **Exit**: 
- Exits the application.

## Database Setup

The project uses **PostgreSQL** to manage user, category, and transaction data. You must set up your database before running the application. 

### Example SQL Queries:

- **Create Users Table**:
```sql
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
```

- **Create Categories Table**:
```sql
CREATE TABLE IF NOT EXISTS categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);
```

- **Create Transactions Table**:
```sql
CREATE TABLE IF NOT EXISTS transactions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    category_id INTEGER REFERENCES categories(id),
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    amount NUMERIC NOT NULL,
    type VARCHAR(50) CHECK (type IN ('income', 'expense')),
    description TEXT
);
```

## Contribution

If you want to contribute to the project:

1. Fork the repository
2. Create a new branch for your feature (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a pull request
