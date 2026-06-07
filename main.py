from app import app
import logging
import threading
import time
from db_utils import create_data_base
import colorama

BASE_URL = "http://127.0.0.1:5000"       # set base url

# Flask run function
def start_flask():

    # Hide log when run.
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    app.run(debug=False)

# Function for posting registration info to API
def post_register_info():
    pass

#Function for posting longin info to API
def post_login_info():
    pass

# Function to interact with API
def run():

    # set required urls here to view. Below are the example url extensions.
    url_view_journal = f"{BASE_URL}/view_journal"
    url_search = f"{BASE_URL}/search"

    # Print Main Menu
    print(colorama.Fore.BLUE +"\n WELCOME TO KindMind SYSTEM!!\n")
    print(colorama.Fore.YELLOW + "a. To Register enter " + colorama.Fore.RED + " 1"+ colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW +"b. To Login enter " + colorama.Fore.RED + " 2"+ colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW +"c. To Exit the system enter"+ colorama.Fore.RED + " 3"+colorama.Style.RESET_ALL)

    # Perform user action
    while True:
        user_input = input(colorama.Fore.LIGHTBLUE_EX +"\nENTER YOUR CHOICE HERE: "+colorama.Style.RESET_ALL)

        if user_input == "1":
            post_register_info() # call post_register_info() declared above to post registration info.
            break

        elif user_input == "2":
            post_login_info() # call post_login_info() function declared above above to post login info.
            break

        elif user_input == "3":
            print(
                colorama.Fore.CYAN + "Thank you for using" + colorama.Fore.BLUE + " KindMind" + colorama.Style.RESET_ALL)
            exit()



# Main function creates database first and then runs flask app to interact with API
if __name__ == "__main__":
    # 1. Create DB first (must complete before anything else)
    create_data_base()

    # 2. Start Flask in background thread
    flask_thread = threading.Thread(target=start_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Delay to ensure Flask runs first before continuing
    time.sleep(2)

    # 3. Run main app.py logic
    try:
        run()
    except KeyboardInterrupt:
        print("\nExited KindMind System")






