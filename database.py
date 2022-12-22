import sqlite3
from infographic import generate_weekly_summary, generate_comprehensive_summary

conn = sqlite3.connect("tasks.db")
conn = sqlite3.connect("users.db")
cursor = conn.cursor()

# Create users table if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS users (chat_id integer)")

# Retrieve all chat IDs from the database
USER_CHAT_IDS = cursor.execute("SELECT chat_id FROM users").fetchall()

# Create tasks table if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (name text, description text, date text, status text)")

# Create habits table if it doesn't exist
cursor.execute("CREATE TABLE IF NOT EXISTS habits (name text, description text, date text, status text)")

def create_task(name, description, date, status, type, bot=None, chat_id=None):
    try:
        if type == "task":
            cursor.execute("INSERT INTO tasks VALUES (?, ?, ?, ?)", (name, description, date, status))
        elif type == "habit":
            cursor.execute("INSERT INTO habits VALUES (?, ?, ?, ?)", (name, description, date, status))
        else:
            print("Invalid type. Please try again.")
            create_task(name, description, date, status, type)
        
        conn.commit()
        
        if bot:
            bot.send_message(chat_id, "Task or habit created successfully! Keep up the good work!")
        else:
            print("Task or habit created successfully! Keep up the good work!")
    except Exception as e:
        print("An error occurred:", e)

def view_list(bot=None, chat_id=None):
    tasks = cursor.execute("SELECT * FROM tasks").fetchall()
    habits = cursor.execute("SELECT * FROM habits").fetchall()
    
    if bot:
        task_message = "Tasks:\n"
        habit_message = "Habits:\n"
        for task in tasks:
            task_message += f"{task[0]}: {task[3]}\n"
        for habit in habits:
            habit_message += f"{habit[0]}: {habit[3]}\n"
        bot.send_message(chat_id, task_message)
        bot.send_message(chat_id, habit_message)
    else:
        print("Tasks:")
        for task in tasks:
            print(f"{task[0]}: {task[3]}")
        print("Habits:")
        for habit in habits:
            print(f"{habit[0]}: {habit[3]}")

def update_status(name, type, status, bot=None, chat_id=None):
    try:
        if type == "task":
            cursor.execute("UPDATE tasks SET status=? WHERE name=?", (status, name))
        elif type == "habit":
            cursor.execute("UPDATE habits SET status=? WHERE name=?", (status, name))
        else:
            print("Invalid type. Please try again.")
            update_status(name, type, status)
        
        conn.commit()
        
        if bot:
            bot.send_message(chat_id, "Task or habit status updated successfully! Keep up the good work!")
        else:
            print("Task or habit status updated successfully! Keep up the good work!")
    except Exception as e:
        print("An error occurred:", e)
        
def delete_task(name, type, bot=None, chat_id=None):
    try:
        if type == "task":
            cursor.execute("DELETE FROM tasks WHERE name=?", (name,))
        elif type == "habit":
            cursor.execute("DELETE FROM habits WHERE name=?", (name,))
        else:
            print("Invalid type. Please try again.")
            delete_task(name, type)
        
        conn.commit()
        
        if bot:
            bot.send_message(chat_id, "Task or habit deleted successfully! Keep up the good work!")
        else:
            print("Task or habit deleted successfully! Keep up the good work!")
    except Exception as e:
        print("An error occurred:", e)

def create_user(chat_id):
    try:
        cursor.execute("INSERT INTO users VALUES (?)", (chat_id,))
        conn.commit()
        print("User created successfully!")
    except Exception as e:
        print("An error occurred:", e)

def delete_user(chat_id):
    try:
        cursor.execute("DELETE FROM users WHERE chat_id=?", (chat_id,))
        conn.commit()
        print("User deleted successfully!")
    except Exception as e:
        print("An error occurred:", e)

def main_menu(bot=None, chat_id=None):
    options = [
    "Create a new task or habit",
    "View current task and habit list",
    "Update the status of a task or habit",
    "Delete a task or habit",
    "Generate a weekly summary infographic",
    "Generate a comprehensive summary infographic",
    "Quit"
    ]
    if bot:
        message = "Please select an option:\n"
        for i, option in enumerate(options):
            message += f"{i+1}. {option}\n"
        bot.send_message(chat_id, message)
    else:
        print("Please select an option:")
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")

    choice = input("Enter your choice: ")
    if choice == "1":
        create_task(bot=bot, chat_id=chat_id)
    elif choice == "2":
        view_list(bot=bot, chat_id=chat_id)
    elif choice == "3":
        update_status(bot=bot, chat_id=chat_id)
    elif choice == "4":
        delete_task(bot=bot, chat_id=chat_id)
    elif choice == "5":
        generate_weekly_summary(bot=bot, chat_id=chat_id)
    elif choice == "6":
        generate_comprehensive_summary(bot=bot, chat_id=chat_id)
    elif choice == "7":
        return
    else:
        print("Invalid choice. Please try again.")
        main_menu(bot=bot, chat_id=chat_id)
