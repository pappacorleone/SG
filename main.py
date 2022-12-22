import logging

@run_async
def main():
    # Connect to the database and create tables if necessary
    connect_to_database()
    
    # Set up logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # Set up the updater and dispatcher
    updater = Updater(TOKEN)
    global dispatcher
    dispatcher = updater.dispatcher
    
    # Add the handlers
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(button_handler)
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occurred:", e)
        exit(1)
