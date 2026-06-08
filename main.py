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

def post_login_info():
    if_logged_in = True #Temporarily set to TRUE
    #Let to implement login function
    if if_logged_in:
        login_menu()
    else:
        print("Invalid Credentials")


def login_menu():

    print(colorama.Fore.RED + "\nYOU HAVE SUCCESSFULLY LOGGED IN")
    print(colorama.Fore.YELLOW + "\na. To Add an Entry to Journal enter " + colorama.Fore.RED + " 1" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "b. To View Journal Entries enter " + colorama.Fore.RED + " 2" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "c. To Edit Journal Entry enter " + colorama.Fore.RED + " 3" + colorama.Style.RESET_ALL)
    print( colorama.Fore.YELLOW + "d. To Search Entries enter " + colorama.Fore.RED + " 4" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "e. To Get Recommendations enter " + colorama.Fore.RED + " 5" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "f. To View Mood Summary enter " + colorama.Fore.RED + " 6" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "g. To Delete an Entry enter  " + colorama.Fore.RED + " 7" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "h. To Logout enter " + colorama.Fore.RED + " 8" + colorama.Style.RESET_ALL)

    login_input = input(colorama.Fore.LIGHTBLUE_EX + "\nENTER YOUR CHOICE HERE: " + colorama.Style.RESET_ALL)

    if login_input == "1":
        add_journal_entry()

    elif login_input == "2":
        view_journal_entry()

    elif login_input == "3":
        edit_journal_entry()

    elif login_input == "4":
        search_entries()

    elif login_input == "5":
        get_recommendations()

    elif login_input == "6":
        to_view_mood_summary()

    elif login_input == "7":
        delete_entry()

    elif login_input == "8":
        logout()


def post_registration_info():
    pass

def view_journal_entry():
    pass

def add_journal_entry():
    print("Add journal entry")

    title = input("Enter a title: ")
    content = input("Write your journal entry: ")

    print("\nChoose your mood:")
    print("1. Happy")
    print("2. Sad")
    print("3. Stressed")
    print("4. Calm")

    mood_choice = input("Enter mood choice: ")

    print("\n---------- Journal Entry ------------")
    print(title)
    print(content)
    print(mood_choice)

def edit_journal_entry():
    pass

def search_entries():
    pass

def get_recommendations():
    pass

def to_view_mood_summary():
    pass

def delete_entry():
    pass

def logout():
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
            post_registration_info() # call post_register_info() declared above to post registration info.
            break

        elif user_input == "2":
            post_login_info()
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






