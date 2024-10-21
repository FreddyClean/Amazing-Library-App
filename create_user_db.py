import sqlite3

# Database file path (it will create user_data.db in the same directory as the script)
DB_PATH = 'user_data.db'

def create_user_database():
    """Create the SQLite database and the users table."""
    try:
        # Connect to the SQLite database (creates the file if it doesn't exist)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create the users table with an auto-increment ID and unique username
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL
            )
        ''')

        # Save the changes and close the connection
        conn.commit()
        print("Database and users table created successfully.")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    create_user_database()