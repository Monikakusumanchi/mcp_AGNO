import gradio as gr
import sqlite3
from agno.tools import Toolkit
from agno.tools import tool  # Required to wrap your functions as tools

# --- DB Functions ---
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

# --- Tool Wrappers ---
@tool(show_result=True, stop_after_tool_call=True)
def insert_user_tool(user_id: int, name: str, task: str, description: str):
    insert_user(user_id, name, task, description)
    return f"User {name} added successfully."

@tool(show_result=True, stop_after_tool_call=True)
def read_users_tool():
    users = read_users()
    return "\n".join([f"{uid}: {name} | {task} - {desc}" for uid, name, task, desc in users])

@tool(show_result=True, stop_after_tool_call=True)
def letter_counter(word: str, letter: str):
    return word.lower().count(letter.lower())

# --- Init DB ---
init_user_db()

# --- Define Toolkit ---
toolkit = [insert_user_tool, read_users_tool, letter_counter]

# --- Launch MCP Gradio App ---
# gr.Interface(
#     fn=toolkit,  # Toolkit as MCP agent
#     inputs="text",
#     outputs="text",
#     title="SQL Agent",
#     description="Perform SQL operations (insert/read) and count letters",
# ).launch(mcp_server=True, mcp_toolkit=toolkit)

# --- Tabbed Gradio Interfaces ---
tabbed = gr.TabbedInterface(
    interface_list=[
        gr.Interface(
            fn=insert_user_tool.entrypoint,
            inputs=[
                gr.Number(label="User ID"),
                gr.Textbox(label="Name"),
                gr.Textbox(label="Task"),
                gr.Textbox(label="Description")
            ],
            outputs=gr.Textbox(label="Result"),
            title="Insert User"
        ),
        gr.Interface(
            fn=read_users_tool.entrypoint,
            inputs=[],
            outputs=gr.Textbox(label="Users"),
            title="Read Users"
        ),
        gr.Interface(
            fn=letter_counter.entrypoint,
            inputs=[
                gr.Textbox(label="Word"),
                gr.Textbox(label="Letter")
            ],
            outputs=gr.Number(label="Letter Count"),
            title="Letter Counter"
        ),
    ],
    tab_names=["Insert", "Read", "Count Letters"]
)

tabbed.launch(mcp_server=True)
