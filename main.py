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
    print("\nAdd journal entry")

    # Ask the user for the journal title and main journal content.
    # This information will eventually be stored in the journal_entries table.
    title = input("Enter a title: ")
    content = input("Write your journal entry: ")

    # Display the mood categories available to the user.
    # These options match the values stored in the mood_category table.
    print("\nChoose your mood category:")
    print("1. Negative")
    print("2. Neutral")
    print("3. Positive")
    print("4. Ambiguous")

    mood_category_choice = input("Enter mood category choice: ")

    # Convert the user's menu selection into both:
    # 1. A user-friendly mood category name.
    # 2. The matching mood_category_id that will later be sent to the database.
    if mood_category_choice == "1":
        mood_category_id = 1
        mood_category = "Negative"
    elif mood_category_choice == "2":
        mood_category_id = 2
        mood_category = "Neutral"
    elif mood_category_choice == "3":
        mood_category_id = 3
        mood_category = "Positive"
    elif mood_category_choice == "4":
        mood_category_id = 4
        mood_category = "Ambiguous"
    else:
        mood_category_id = None
        mood_category = "Unknown"

    # Display mood score options from the mood_score table.
    # The user selects a number and we store both the score name and ID.
    print("\nChoose your mood score:")
    print("1. Terrible")
    print("2. Bad")
    print("3. Off")
    print("4. Ok")
    print("5. Good")
    print("6. Great")
    print("7. Fantastic")
    print("8. Mixed")
    print("9. Unsure")

    mood_score_choice = input("Enter mood score choice: ")

    # Convert the user's mood score selection into both:
    # 1. A descriptive mood score.
    # 2. The matching mood_score_id for future database integration.
    if mood_score_choice == "1":
        mood_score_id = 1
        mood_score = "Terrible"
    elif mood_score_choice == "2":
        mood_score_id = 2
        mood_score = "Bad"
    elif mood_score_choice == "3":
        mood_score_id = 3
        mood_score = "Off"
    elif mood_score_choice == "4":
        mood_score_id = 4
        mood_score = "Ok"
    elif mood_score_choice == "5":
        mood_score_id = 5
        mood_score = "Good"
    elif mood_score_choice == "6":
        mood_score_id = 6
        mood_score = "Great"
    elif mood_score_choice == "7":
        mood_score_id = 7
        mood_score = "Fantastic"
    elif mood_score_choice == "8":
        mood_score_id = 8
        mood_score = "Mixed"
    elif mood_score_choice == "9":
        mood_score_id = 9
        mood_score = "Unsure"
    else:
        mood_score_id = None
        mood_score = "Unknown"

    # Collect the user's current energy level.
    # This will help support recommendations and mood analytics later.
    print("\nChoose your energy level:")
    print("1. Drained")
    print("2. Sluggish")
    print("3. Mellow")
    print("4. Steady")
    print("5. Vibrant")
    print("6. Driven")
    print("7. Radiant")

    energy_choice = input("Enter energy level choice: ")

    if energy_choice == "1":
        energy_level_id = 1
        energy_level = "Drained"
    elif energy_choice == "2":
        energy_level_id = 2
        energy_level = "Sluggish"
    elif energy_choice == "3":
        energy_level_id = 3
        energy_level = "Mellow"
    elif energy_choice == "4":
        energy_level_id = 4
        energy_level = "Steady"
    elif energy_choice == "5":
        energy_level_id = 5
        energy_level = "Vibrant"
    elif energy_choice == "6":
        energy_level_id = 6
        energy_level = "Driven"
    elif energy_choice == "7":
        energy_level_id = 7
        energy_level = "Radiant"
    else:
        energy_level_id = None
        energy_level = "Unknown"

    # Ask whether the user has free time available.
    # This may be used later when suggesting wellbeing activities.
    print("\nDo you have free time today?")
    print("1. Yes")
    print("2. No")

    free_time_choice = input("Enter free time choice: ")

    # Store the value as True or False because this is easier
    # to save in the database later.
    #
    # We also create a separate display value ("Yes" or "No")
    # so the user sees something more readable on screen.
    if free_time_choice == "1":
        free_time = True
        free_time_display = "Yes"
    elif free_time_choice == "2":
        free_time = False
        free_time_display = "No"
    else:
        free_time = None
        free_time_display = "Unknown"

    # TODO:
    # Weather will be retrieved automatically from the weather API
    # rather than entered manually by the user.

    # Display a summary of all information entered so the user can
    # review their journal entry before it is saved.
    print("\n---------- Journal Entry ------------")
    print(f"Title: {title}")
    print(f"Content: {content}")
    print(f"Mood Category: {mood_category}")
    print(f"Mood Score: {mood_score}")
    print(f"Energy Level: {energy_level}")
    print(f"Free Time: {free_time_display}")

    # TODO:
    # Send the collected data to the API/database once integration is complete.
    # Data to be stored includes:
    # title
    # content
    # mood_category_id
    # mood_score_id
    # energy_level_id
    # free_time
    # weather

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






