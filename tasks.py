import datetime

def create_task(bot=None, chat_id=None):
    try:
        name = input("Enter the name of the task or habit: ")
        type = input("Enter the type of the task or habit (task, habit): ")
        if type == "task":
            date = datetime.now().strftime("%Y-%m-%d")
            status = "not started"
            cursor.execute("INSERT INTO tasks VALUES (?, ?, ?, ?)", (name, type, date, status))
        elif type == "habit":
            frequency = input("Enter the frequency of the habit (daily, weekly): ")
            date = datetime.now().strftime("%Y-%m-%d")
            status = "not started"
            cursor.execute("INSERT INTO habits VALUES (?, ?, ?, ?)", (name, frequency, date, status))
        else:
            print("Invalid type. Please try again.")
            create_task()
        
        conn.commit()
        
        if bot:
            bot.send_message(chat_id, "Task or habit added successfully! Keep up the good work!")
        else:
            print("Task or habit added successfully! Keep up the good work!")
        
        main_menu()
    except Exception as e:
        print("An error occurred:", e)
        main_menu()
        
def view_list(bot=None, chat_id=None):
    tasks = cursor.execute("SELECT * FROM tasks").fetchall()
    habits = cursor.execute("SELECT * FROM habits").fetchall()
    
    if not tasks and not habits:
        if bot:
            bot.send_message(chat_id, "Your task and habit list is currently empty. Get started by creating a new task or habit!")
        else:
            print("Your task and habit list is currently empty. Get started by creating a new task or habit!")
    else:
        message = "Tasks:\n"
        for task in tasks:
            message += f" - {task[0]}: {task[3]}\n"
        
        message += "\nHabits:\n"
        for habit in habits:
            message += f" - {habit[0]}: {habit[3]}\n"
        
        if bot:
            bot.send_message(chat_id, message)
        else:
            print(message)
    
    main_menu()
    
 def update_status(botdef update_status(bot=None, chat_id=None):
    try:
        name = input("Enter the name of the task or habit: ")
        type = input("Enter the type of the task or habit (task, habit): ")
        if type == "task":
            status = input("Enter the new status of the task (not started, in progress, completed): ")
            cursor.execute("UPDATE tasks SET status=? WHERE name=?", (status, name))
        elif type == "habit":
            status = input("Enter the new status of the habit (not started, in progress, completed): ")
            cursor.execute("UPDATE habits SET status=? WHERE name=?", (status, name))
        else:
            print("Invalid type. Please try again.")
            update_status()
        
        conn.commit()
    
        if bot:
            bot.send_message(chat_id, "Task or habit status updated successfully! Keep up the good work!")
        else:
            print("Task or habit status updated successfully! Keep up the good work!")

        main_menu()
    except Exception as e:
        print("An error occurred:", e)
        main_menu()
                   
  def delete_task(bot=None, chat_id=None):
    try:
        name = input("Enter the name of the task or habit to delete: ")
        type = input("Enter the type of the task or habit (task, habit): ")
        if type == "task":
            cursor.execute("DELETE FROM tasks WHERE name=?", (name,))
        elif type == "habit":
            cursor.execute("DELETE FROM habits WHERE name=?", (name,))
        else:
            print("Invalid type. Please try again.")
            delete_task()
        
        conn.commit()
        
        if bot:
            bot.send_message(chat_id, "Task or habit deleted successfully! Keep up the good work!")
        else:
            print("Task or habit deleted successfully! Keep up the good work!")
        
        main_menu()
    except Exception as e:
        print("An error occurred:", e)
        main_menu()

def send_daily_summary(bot, chat_id):
    tasks = cursor.execute("SELECT * FROM tasks WHERE date=?", (datetime.now().strftime("%Y-%m-%d"),)).fetchall()
    habits = cursor.execute("SELECT * FROM habits WHERE date=?", (datetime.now().strftime("%Y-%m-%d"),)).fetchall()
    
    generate_weekly_summary(tasks, habits)
    bot.send_photo(chat_id, open("weekly_summary.png", "rb"))

def send_weekly_summary(bot, chat_id):
    tasks = cursor.execute("SELECT * FROM tasks").fetchall()
    habits = cursor.execute("SELECT * FROM habits").fetchall()
    
    generate_comprehensive_summary(tasks, habits)
    bot.send_photo(chat_id, open("comprehensive_summary.png", "rb"))



