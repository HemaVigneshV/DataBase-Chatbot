import sqlite3
import tkinter as tk
from tkinter import scrolledtext
from tabulate import tabulate

# SQLite functions for each operation
def create_table(table_name, columns):
    conn = sqlite3.connect(f"{table_name}.db")
    cursor = conn.cursor()
    column_definitions = ", ".join([f"{col} TEXT" for col in columns])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})")
    conn.commit()
    conn.close()

def insert_values(table_name, values):
    conn = sqlite3.connect(f"{table_name}.db")
    cursor = conn.cursor()
    placeholders = ", ".join(["?" for _ in values])
    cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", values)
    conn.commit()
    conn.close()

def update_table(table_name, updates, condition):
    conn = sqlite3.connect(f"{table_name}.db")
    cursor = conn.cursor()
    update_statements = ", ".join(updates)
    cursor.execute(f"UPDATE {table_name} SET {update_statements} WHERE {condition}")
    conn.commit()
    conn.close()

def delete_from_table(table_name, condition):
    conn = sqlite3.connect(f"{table_name}.db")
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name} WHERE {condition}")
    conn.commit()
    conn.close()

def select_from_table(table_name, columns, condition):
    conn = sqlite3.connect(f"{table_name}.db")
    cursor = conn.cursor()
    columns_str = ", ".join(columns)
    cursor.execute(f"SELECT {columns_str} FROM {table_name} WHERE {condition}")
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        # Use tabulate to format the output as a table
        table = tabulate(rows, headers=columns, tablefmt="grid")
        return f"Selected rows:\n{table}"
    else:
        return f"No matching rows found in '{table_name}'"

# Function to process user input and generate bot responses
def process_input(sentence):
    try:
        # Create Table - 3 Alternative Statements
        if sentence.startswith("Create a table named") or sentence.startswith("Build a new table called") or sentence.startswith("Make a table with name"):
            parts = sentence.split(" with columns ")
            table_name = parts[0].split(" ")[-1]  # Extract table name
            columns = parts[1].split(", ")
            create_table(table_name, columns)
            return f"Table '{table_name}' created with columns {columns}"
        
        # Insert Values - 3 Alternative Statements
        elif sentence.startswith("Insert values") or sentence.startswith("Add records") or sentence.startswith("Put data"):
            parts = sentence.split(" into ")
            values = parts[0].replace("Insert values ", "").replace("Add records ", "").replace("Put data ", "").split(", ")
            table_name = parts[1]
            insert_values(table_name, values)
            return f"Inserted values {values} into '{table_name}'"
        
        # Update Table - 3 Alternative Statements
        elif sentence.startswith("Update") or sentence.startswith("Modify table") or sentence.startswith("Change records in"):
            parts = sentence.split(" set ")
            table_name = parts[0].split(" ")[-1]  # Extract table name
            set_part = parts[1].split(" where ")
            updates = set_part[0].split(", ")
            condition = set_part[1]
            update_table(table_name, updates, condition)
            return f"Updated table '{table_name}' with {updates} where {condition}"
        
        # Delete from Table - 3 Alternative Statements
        elif sentence.startswith("Delete from") or sentence.startswith("Remove records from") or sentence.startswith("Erase from"):
            parts = sentence.split(" where ")
            table_name = parts[0].replace("Delete from ", "").replace("Remove records from ", "").replace("Erase from ", "")
            condition = parts[1]
            delete_from_table(table_name, condition)
            return f"Deleted from '{table_name}' where {condition}"
        
        # Select from Table - 3 Alternative Statements
        elif sentence.startswith("Select") or sentence.startswith("Retrieve data") or sentence.startswith("Fetch"):
            parts = sentence.split(" from ")
            columns = parts[0].replace("Select ", "").replace("Retrieve data ", "").replace("Fetch ", "").split(", ")
            condition_part = parts[1].split(" where ")
            table_name = condition_part[0]
            condition = condition_part[1]
            return select_from_table(table_name, columns, condition)
        
        else:
            return "Sorry, I couldn't understand your command."
    
    except Exception as e:
        return f"Error: {str(e)}"


# Tkinter interface resembling ChatGPT UI
class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SQLite3 Chatbot - ChatGPT UI")

        # Scrollable chat display
        self.chat_display = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=20, width=60, state='disabled', bg="#f0f0f0")
        self.chat_display.grid(column=0, row=0, padx=10, pady=10)

        # User input box
        self.user_input = tk.Entry(self.root, width=50)
        self.user_input.grid(column=0, row=1, padx=10, pady=5, sticky="w")
        self.user_input.bind("<Return>", self.handle_user_input)  # Enter key to send message

        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.handle_user_input)
        self.send_button.grid(column=0, row=1, padx=10, pady=5, sticky="e")

    def handle_user_input(self, event=None):
        user_text = self.user_input.get().strip()
        if user_text.lower() == "exit":
            self.root.quit()

        self.display_message(f"You: {user_text}", user=True)
        self.user_input.delete(0, tk.END)

        # Process input and generate response
        response = process_input(user_text)
        self.display_message(f"Bot: {response}", user=False)
    
    def display_message(self, message, user=True):
        self.chat_display.configure(state='normal')
        if user:
            self.chat_display.insert(tk.END, f"{message}\n", "user")
        else:
            self.chat_display.insert(tk.END, f"{message}\n", "bot")
        self.chat_display.configure(state='disabled')
        self.chat_display.yview(tk.END)

# Custom styling to differentiate User and Bot messages
def apply_custom_styles(chat_display):
    chat_display.tag_configure("user", foreground="blue", font=("Arial", 10, "bold"))
    chat_display.tag_configure("bot", foreground="green", font=("Arial", 10, "italic"))

# Run the Tkinter app
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotApp(root)
    apply_custom_styles(app.chat_display)
    root.mainloop()
