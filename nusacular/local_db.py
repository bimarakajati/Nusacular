import sqlite3

# Function to create the database table if it doesn't exist
def create_table():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        role TEXT,
        content TEXT
    )
    """)
    conn.commit()
    conn.close()

# Function to insert a message into the database
def insert_message(role, content):
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO chat_history (role, content) VALUES (?, ?)", (role, content))
    conn.commit()
    conn.close()

# Function to retrieve messages from the database
def retrieve_messages():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chat_history")
    messages = cursor.fetchall()
    conn.close()
    return messages

# Function to clear the database
def clear_database():
    conn = sqlite3.connect("chat_history.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM chat_history")
    conn.commit()
    conn.close()

# Create the database table if it doesn't exist
create_table()