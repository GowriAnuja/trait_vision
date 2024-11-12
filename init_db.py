import sqlite3

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

# Create the products table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT NOT NULL,
        price REAL NOT NULL,
        time_period TEXT NOT NULL,
        image TEXT NOT NULL
    )
''')

connection.commit()
connection.close()

print("Database initialized and table created successfully.")
