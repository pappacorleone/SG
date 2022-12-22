import telegram
import tasks
import database
import datetime

bot = telegram.Bot(token=5879721167:AAEl1EzoHTbLNJOHKeYJt_KlxzgBAsyaozU)

def handle_input(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    
    if text == "/start":
        bot.send_message(chat_id, "Welcome to the Motivational Coaching Chatbot! Please select an option from the menu below:")
        tasks.main_menu(bot, chat_id)
    elif text == "1. Create a new task or habit":
        tasks.create_task(bot, chat_id)
    elif text == "2. View my task and habit list":
        tasks.view_list(bot, chat_id)
    elif text == "3. Update the status of a task or habit":
        tasks.update_status(bot, chat_id)
    elif text == "4. Delete a task or habit":
        tasks.delete_task(bot, chat_id)
    else:
        bot.send_message(chat_id, "Invalid input. Please select a valid option from the menu.")
        tasks.main_menu(bot, chat_id)

def check_daily_reminders(bot, job):
    if datetime.now().strftime("%A") == "Sunday":
        tasks = cursor.execute("SELECT * FROM tasks WHERE date < ?", (datetime.now().strftime("%Y-%m-%d"),)).fetchall()
        habits = cursor.execute("SELECT * FROM habits WHERE date < ?", (datetime.now().strftime("%Y-%m-%d"),)).fetchall()
        
        for task in tasks:
            database.create_task(task[0], task[1], datetime.now().strftime("%Y-%m-%d"), task[3], "task")
        for habit in habits:
            database.create_task(habit[0], habit[1], datetime.now().strftime("%Y-%m-%d"), habit[3], "habit")
    else:
        tasks = cursor.execute("SELECT * FROM tasks WHERE date=?", (datetime.now().strftime("%Y-%m-%d"),)).fetchall()
        habits = cursor.execute("SELECT * FROM habits WHERE date=?", (datetime.now().strftime("%Y-%m-%d"),)).fetchall()
        
        if tasks or habits:
            for user in USER_CHAT_IDS:
                bot.send_message(user, "Don't forget to update your tasks and habits for the day!")

updater = telegram.ext.Updater(bot)
updater.dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_input))

job_queue = updater.job_queue
job_queue.run_repeating(check_daily_reminders, interval=86400, first=0)

updater.start_polling()
