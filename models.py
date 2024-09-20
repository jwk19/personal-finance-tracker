

import psycopg2
from db import get_connection

class User:
    def __init__(self, name, user_id=None):
        self.user_id = user_id
        self.name = name

    def save(self):
        """Insert a new user into the database"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name) VALUES (%s) RETURNING id;", (self.name,))
        self.user_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get(user_id):
        """Retrieve a user by ID"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM users WHERE id = %s;", (user_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return User(name=row[1], user_id=row[0])
        return None

    @staticmethod
    def delete(user_id):
        """Delete a user from the database"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM users WHERE id = %s;", (user_id,))
        conn.commit()
        cur.close()
        conn.close()

    def __repr__(self):
        return f"<User(id={self.user_id}, name={self.name})>"


# category class

class Category:
    def __init__(self, name, category_id=None):
        self.category_id = category_id
        self.name = name

    def save(self):
        """Insert a new category into the database"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO categories (name) VALUES (%s) ON CONFLICT DO NOTHING RETURNING id;", (self.name,))
        result = cur.fetchone()
        if result:
            self.category_id = result[0]
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get(category_id):
        """Retrieve a category by ID"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, name FROM categories WHERE id = %s;", (category_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if row:
            return Category(name=row[1], category_id=row[0])
        return None

    @staticmethod
    def delete(category_id):
        """Delete a category from the database"""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM categories WHERE id = %s;", (category_id,))
        conn.commit()
        cur.close()
        conn.close()

    def __repr__(self):
        return f"<Category(id={self.category_id}, name={self.name})>"

# transctions class

from db import get_connection
from datetime import date

class Transaction:
    def __init__(self, user_id, category_id, amount, type, description="", date=None, transaction_id=None):
        self.transaction_id = transaction_id
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
        self.type = type
        self.description = description
        self.date = date if date else None  # Allow database default if date is not provided

    def save(self):
        """Insert a new transaction into the database."""
        conn = get_connection()
        cur = conn.cursor()

        # If a date is provided, include it in the insert, otherwise use the database default
        if self.date:
            cur.execute("""
                INSERT INTO transactions (user_id, category_id, amount, type, description, date)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;
            """, (self.user_id, self.category_id, self.amount, self.type, self.description, self.date))
        else:
            cur.execute("""
                INSERT INTO transactions (user_id, category_id, amount, type, description)
                VALUES (%s, %s, %s, %s, %s) RETURNING id;
            """, (self.user_id, self.category_id, self.amount, self.type, self.description))

        self.transaction_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get(transaction_id):
        """Retrieve a transaction by ID."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, user_id, category_id, amount, type, description, date
            FROM transactions WHERE id = %s;
        """, (transaction_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if row:
            return Transaction(
                transaction_id=row[0], user_id=row[1], category_id=row[2],
                amount=row[3], type=row[4], description=row[5], date=row[6]
            )
        return None

    @staticmethod
    def delete(transaction_id):
        """Delete a transaction from the database."""
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM transactions WHERE id = %s;", (transaction_id,))
        conn.commit()
        cur.close()
        conn.close()

    def __repr__(self):
        return f"<Transaction(id={self.transaction_id}, user_id={self.user_id}, amount={self.amount}, type={self.type})>"

