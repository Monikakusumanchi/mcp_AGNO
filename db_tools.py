from agno.tools import tool
import sqlite3

# DB logic
def init_user_db():
    conn = sqlite3.connect("letter_counts.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            task TEXT NOT NULL,
            description TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_user(user_id: int, name: str, task: str, description: str):
    conn = sqlite3.connect("letter_counts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, name, task, description) VALUES (?, ?, ?, ?)", 
                   (user_id, name, task, description))
    conn.commit()
    conn.close()

def read_users():
    conn = sqlite3.connect("letter_counts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, task, description FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows


@tool(name="InsertUser", description="Insert a user into the users table with id, name, task, and description")
def insert_user_tool(user_id: int, name: str, task: str, description: str):
    insert_user(user_id, name, task, description)
    return f"User {name} added successfully."

@tool(name="ReadUsers", description="Read all users from the users table")
def read_users_tool():
    users = read_users()
    return "\n".join([f"{uid}: {name} | {task} - {desc}" for uid, name, task, desc in users])

