from app import app
import logging
import threading
import time
from db_utils import create_database, get_logged_in_user_id
import colorama
import requests
from dotenv import load_dotenv
import os
import re
load_dotenv()

BASE_URL = "http://127.0.0.1:5000"       # set base url

# Flask run function
def start_flask():

    # Hide log when run.
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    app.run(debug=False)


def get_current_weather(current_city):

    api_key = os.getenv("WEATHER_API_KEY")
    city = current_city

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )

    try:
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()

        if "weather" in data:
            return data["weather"][0]["main"]
        return None

    except requests.RequestException:
        return None

def get_user_input_for_weather():
    city = input("\nEnter your city lets check the weather: ")

    weather = get_current_weather(city)

    return weather



def post_login_info():

    user_email = None
    user_password = None

    password_validation = True
    email_validation = True
    if_logged_in = False

    while email_validation:
        user_email = input("\nEnter your email: ")
        email_validation = validate_user_email(user_email)

    while password_validation:
        user_password = input("\nEnter your password: ")
        password_validation = validate_user_password(user_password)


    log_in_info = {
        "email": user_email,
        "password": user_password
    }

    try:
        response = requests.post(
            f"{BASE_URL}/login",
            json=log_in_info,
            timeout=10
        )

        data = response.json()

        if response.status_code == 200:
            print(f"\nLogging In: {data.get('message')}")
            if_logged_in = True

        else:
            print(f"\nLogin failed: {data.get('errors')}")

    except requests.exceptions.ConnectionError:
        print("Could not connect to API server.")

    except Exception as e:
        print(f"Error: {e}")

    if if_logged_in:
        logged_in_id=get_logged_in_user_id(user_email)
        login_menu(logged_in_id)


def login_menu(logged_in_id):

    print(colorama.Fore.YELLOW + "\na. To Add an Entry to Journal enter " + colorama.Fore.RED + " 1" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "b. To View Journal Entries enter " + colorama.Fore.RED + " 2" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "c. To Edit Journal Entry enter " + colorama.Fore.RED + " 3" + colorama.Style.RESET_ALL)
    print( colorama.Fore.YELLOW + "d. To Search Entries enter " + colorama.Fore.RED + " 4" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "e. To Get Recommendations enter " + colorama.Fore.RED + " 5" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "f. To View Mood Summary enter " + colorama.Fore.RED + " 6" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "g. To Delete an Entry enter  " + colorama.Fore.RED + " 7" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "h. To Logout enter " + colorama.Fore.RED + " 8" + colorama.Style.RESET_ALL)

    # Perform user action
    while True:
        login_input = input(colorama.Fore.LIGHTBLUE_EX + "\nENTER YOUR CHOICE HERE: " + colorama.Style.RESET_ALL)

        if login_input == "1":
            add_journal_entry(logged_in_id)
            break

        elif login_input == "2":
            view_journal_entry()
            break

        elif login_input == "3":
            edit_journal_entry()
            break

        elif login_input == "4":
            search_entries(logged_in_id)
            break

        elif login_input == "5":

            print("Choose Today's Mood Category from below:")

            print("\n1. Negative")

            print("2. Neutral")

            print("3. Positive")

            print("4. Ambiguous")

            while True:

                user_mood_category = input("\nEnter Your Mood Category (1-4): ")

                if user_mood_category in ["1", "2", "3", "4"]:
                    break

                print("Invalid choice. Please enter a number between 1 and 4.")

            print(f"You selected option {user_mood_category}")

            print("\nChoose Your mood from:")

            print("\n1. Terrible")

            print("2. Bad")

            print("3. Off")

            print("4. Ok")

            print("5. Good")

            print("6. Great")

            print("7. Fantastic")

            print("8. Mixed")

            print("9. Unsure")

            while True:

                user_mood = input("\nEnter Your Mood (1-9): ")

                if user_mood in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                    break

                print("Invalid choice. Please enter a number between 1 and 9.")

            print(f"You selected option {user_mood}")

            print("\nChoose Your energy level from:")

            print("\n1. Drained")

            print("2. Sluggish")

            print("3. Mellow")

            print("4. Steady")

            print("5. Vibrant")

            print("6. Driven")

            print("7. Radiant")

            while True:

                user_energy = input("\nEnter Your Energy Level (1-7): ")

                if user_energy in ["1", "2", "3", "4", "5", "6", "7"]:
                    break

                print("Invalid choice. Please enter a number between 1 and 7.")

            print(f"You selected option {user_energy}")

            while True:

                user_free_time = input("\nDo you have free Time? (Y/N): ").upper()

                if user_free_time in ["Y", "N"]:
                    break

                print("Invalid choice. Please enter either Y or N.")

            has_free_time = user_free_time == "Y"

            print(f"You selected option {user_free_time}")

            while True:

                weather_result = get_user_input_for_weather()

                if weather_result:
                    break

                print("Please enter a valid city.")
            print(f"Your current weather is {weather_result}")

            # Added Mappings

            mood_categories = {

                "1": "Negative",

                "2": "Neutral",

                "3": "Positive",

                "4": "Ambiguous"

            }

            mood_scores = {

                "1": "Terrible",

                "2": "Bad",

                "3": "Off",

                "4": "Ok",

                "5": "Good",

                "6": "Great",

                "7": "Fantastic",

                "8": "Mixed",

                "9": "Unsure"

            }

            energy_levels = {

                "1": "Drained",

                "2": "Sluggish",

                "3": "Mellow",

                "4": "Steady",

                "5": "Vibrant",

                "6": "Driven",

                "7": "Radiant"

            }

            # Convert id's to Names
            category = mood_categories[user_mood_category]

            mood = mood_scores[user_mood]

            energy = energy_levels[user_energy]


            # Call get_recommendations function
            recommendation_result = get_recommendations(category, mood, energy, has_free_time, weather_result)

            print("\n==============================")

            print("PERSONALIZED RECOMMENDATIONS")

            print("==============================")

            print(recommendation_result)

            break

        elif login_input == "6":
            view_mood_summary(logged_in_id)
            break

        elif login_input == "7":
            delete_entry()
            break

        elif login_input == "8":
            print("You have Successfully Logged Out!")
            exit()

        else:
            print("Invalid Input Please Try Again!")
            continue

def validate_user_name(name):
    if not name.strip():
        print("Name cannot be empty.")
        return True

    if len(name.strip()) < 2:
        print("Name must be at least 2 characters.")
        return True

    if not re.match(r"^[A-Za-z ]+$", name):
        print("Name can only contain letters and spaces.")
        return True

    return False

def validate_user_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, email):
        print("Invalid email format.")
        return True

    return False

def validate_user_password(password):
    if len(password) < 7:
        print("Password must be at least 7 characters.")
        return True

    if not re.search(r"[A-Z]", password):
        print("Password must contain an uppercase letter.")
        return True

    if not re.search(r"[a-z]", password):
        print("Password must contain a lowercase letter.")
        return True

    if not re.search(r"\d", password):
        print("Password must contain a number.")
        return True

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        print("Password must contain a special character.")
        return True
    return False

def post_registration_info():
    print("\n=== USER REGISTRATION ===")

    name = None
    email = None
    password = None

    name_prompt=True
    while name_prompt:
        name = input(colorama.Fore.BLUE +"Name: ").strip()
        name_prompt=validate_user_name(name)

    email_prompt=True
    while email_prompt:
        email = input(colorama.Fore.BLUE +"Email: "+colorama.Style.RESET_ALL).strip()
        email_prompt=validate_user_email(email)

    pwd_prompt=True
    while pwd_prompt:

        print("Pwd must contain at least:")
        print("1. 7 characters")
        print("2. a uppercase letter")
        print("3. a lowercase letter")
        print("4. a special character")
        print("5. a number")
        password = input(colorama.Fore.BLUE +"Password: "+colorama.Style.RESET_ALL)
        pwd_prompt=validate_user_password(password)

    reg_info = {
        "name": name,
        "email": email,
        "password": password
    }

    try:
        response = requests.post(
            f"{BASE_URL}/register",
            json=reg_info,
            timeout=10
        )

        data = response.json()

        if response.status_code == 201:
            print("\nSuccessfully Registered!")
            print("\n======LOGIN==========")
            post_login_info()

        else:
            print(f"\nRegistration failed: {data.get('message')}")

    except requests.exceptions.ConnectionError:
        print("Could not connect to API server.")

    except Exception as e:
        print(f"Error: {e}")

def view_journal_entry():

    # Display the View Journal Entries heading.
    print(
        colorama.Fore.CYAN +
        "\n========== VIEW JOURNAL ENTRIES ==========" +
        colorama.Style.RESET_ALL
    )

    # TODO:
    # Replace this mock data with real journal entries from the database/API
    # once backend integration is ready.
    #
    # Currently this list is only used for testing the Console UI.
    journal_entries = [
        {
            "entry_id": 1,
            "title": "Test Entry 1",
            "content": "Today was a good day.",
            "mood_category": "Positive",
            "mood_score": "Fantastic",
            "energy_level": "Driven",
            "free_time": "Yes",
            "weather": "Rain",
            "recommendations": "Keep up the positive momentum."
        },
        {
            "entry_id": 2,
            "title": "Test Entry 2",
            "content": "Feeling a bit tired today.",
            "mood_category": "Negative",
            "mood_score": "Bad",
            "energy_level": "Drained",
            "free_time": "No",
            "weather": "Clouds",
            "recommendations": "Prioritise rest and hydration."
        }
    ]

    # Check whether any journal entries exist.
    # If the list is empty, notify the user and exit the function.
    if not journal_entries:
        print(
            colorama.Fore.RED +
            "\nNo journal entries found." +
            colorama.Style.RESET_ALL
        )
        return

    # Display all available journal entries so the user can
    # choose which entry they would like to view.
    print(
        colorama.Fore.YELLOW +
        "\nAvailable journal entries:" +
        colorama.Style.RESET_ALL
    )

    for entry in journal_entries:
        print(
            colorama.Fore.CYAN +
            f"{entry['entry_id']}. {entry['title']} - Mood: {entry['mood_category']}" +
            colorama.Style.RESET_ALL
        )

    # Ask the user which journal entry they would like to view.
    # Validation ensures the selected entry ID exists.
    while True:
        entry_choice = input(
            colorama.Fore.LIGHTBLUE_EX +
            "\nEnter the entry ID you want to view: " +
            colorama.Style.RESET_ALL
        )

        # Check that the user entered a number.
        if entry_choice.isdigit():
            entry_choice = int(entry_choice)

            selected_entry = None

            # Search for the journal entry that matches
            # the ID entered by the user.
            for entry in journal_entries:
                if entry["entry_id"] == entry_choice:
                    selected_entry = entry
                    break

            # If a matching entry is found, continue.
            if selected_entry:
                break

        # Display an error message if the selected ID is invalid.
        print(
            colorama.Fore.RED +
            "Invalid entry ID. Please choose an entry from the list." +
            colorama.Style.RESET_ALL
        )

    # Display the full details of the selected journal entry.
    print(
        colorama.Fore.CYAN +
        "\n---------- Selected Journal Entry ------------" +
        colorama.Style.RESET_ALL
    )

    print(colorama.Fore.CYAN + f"Entry ID: {selected_entry['entry_id']}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Title: {selected_entry['title']}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Content: {selected_entry['content']}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Mood Category: {selected_entry['mood_category']}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Mood Score: {selected_entry['mood_score']}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Energy Level: {selected_entry['energy_level']}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Free Time: {selected_entry['free_time']}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Weather: {selected_entry['weather']}" + colorama.Style.RESET_ALL)

    # Display the recommendations associated with the journal entry.
    # These recommendations will eventually come from the database/API.
    print(
        colorama.Fore.GREEN +
        "\nRecommendations:" +
        colorama.Style.RESET_ALL
    )

    print(
        colorama.Fore.GREEN +
        f"{selected_entry['recommendations']}" +
        colorama.Style.RESET_ALL
    )

    # TODO:
    # Retrieve journal entries from the API/database once backend
    # integration is complete rather than using temporary test data.

def add_journal_entry(logged_in_id):

    # Display the Add Journal Entry heading.
    print(colorama.Fore.RED + "\nADD JOURNAL ENTRY" + colorama.Style.RESET_ALL)

    # Collect the journal title from the user.
    # Validation ensures the title cannot be left blank.
    while True:
        title = input(
            colorama.Fore.LIGHTBLUE_EX +
            "Enter a title: " +
            colorama.Style.RESET_ALL
        )

        if title.strip():
            break

        print(
            colorama.Fore.RED +
            "Title cannot be empty. Please try again." +
            colorama.Style.RESET_ALL
        )

    # Collect the journal content from the user.
    # Validation ensures the journal entry is not empty.
    while True:
        content = input(
            colorama.Fore.LIGHTBLUE_EX +
            "Write your journal entry: " +
            colorama.Style.RESET_ALL
        )

        if content.strip():
            break

        print(
            colorama.Fore.RED +
            "Journal content cannot be empty. Please try again." +
            colorama.Style.RESET_ALL
        )

    # Display available mood categories.
    # These values match the mood_category table in the database.
    print(colorama.Fore.YELLOW + "\nChoose your mood category:" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "1. Negative" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "2. Neutral" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "3. Positive" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "4. Ambiguous" + colorama.Style.RESET_ALL)

    while True:
        mood_category_choice = input(
            colorama.Fore.LIGHTBLUE_EX +
            "Enter mood category choice: " +
            colorama.Style.RESET_ALL
        )
        # Validate the user's mood category selection.
        # Only options 1-4 are accepted.
        if mood_category_choice in ["1", "2", "3", "4"]:
            break

        print(
            colorama.Fore.RED +
            "Invalid choice. Please enter a number between 1 and 4." +
            colorama.Style.RESET_ALL
        )

    # Convert the user's menu choice into:
    # 1. A mood category name for display.
    # 2. A mood_category_id for future database storage.
    if mood_category_choice == "1":
        mood_category = "Negative"
    elif mood_category_choice == "2":
        mood_category = "Neutral"
    elif mood_category_choice == "3":
        mood_category = "Positive"
    elif mood_category_choice == "4":
        mood_category = "Ambiguous"
    else:
        mood_category = "Unknown"

    # Display available mood scores.
    # These values match the mood_score table in the database.
    print(colorama.Fore.YELLOW + "\nChoose your mood score:" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "1. Terrible" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "2. Bad" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "3. Off" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "4. Ok" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "5. Good" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "6. Great" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "7. Fantastic" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "8. Mixed" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "9. Unsure" + colorama.Style.RESET_ALL)

    # Validate the user's mood score selection.
    # Only options 1-9 are accepted.
    while True:
        mood_score_choice = input(
            colorama.Fore.LIGHTBLUE_EX +
            "Enter mood score choice: " +
            colorama.Style.RESET_ALL
        )

        # Convert the user's menu choice into:
        # 1. A mood score name for display.
        # 2. A mood_score_id for future database storage.
        if mood_score_choice in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            break

        print(
            colorama.Fore.RED +
            "Invalid choice. Please enter a number between 1 and 9." +
            colorama.Style.RESET_ALL
        )

    # Convert the user's mood score selection into both:
    # 1. A descriptive mood score.
    # 2. The matching mood_score_id for future database integration.
    if mood_score_choice == "1":
        mood_score = "Terrible"
    elif mood_score_choice == "2":
        mood_score = "Bad"
    elif mood_score_choice == "3":
        mood_score = "Off"
    elif mood_score_choice == "4":
        mood_score = "Ok"
    elif mood_score_choice == "5":
        mood_score = "Good"
    elif mood_score_choice == "6":
        mood_score = "Great"
    elif mood_score_choice == "7":
        mood_score = "Fantastic"
    elif mood_score_choice == "8":
        mood_score = "Mixed"
    elif mood_score_choice == "9":
        mood_score = "Unsure"
    else:
        mood_score = "Unknown"

    # Display available energy levels.
    # These values match the energy_level table in the database.
    print(colorama.Fore.YELLOW + "\nChoose your energy level:" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "1. Drained" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "2. Sluggish" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "3. Mellow" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "4. Steady" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "5. Vibrant" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "6. Driven" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "7. Radiant" + colorama.Style.RESET_ALL)

    # Validate the user's energy level selection.
    # Only options 1-7 are accepted.
    while True:
        energy_choice = input(
            colorama.Fore.LIGHTBLUE_EX +
            "Enter energy level choice: " +
            colorama.Style.RESET_ALL
        )

        if energy_choice in ["1", "2", "3", "4", "5", "6", "7"]:
            break

        print(
            colorama.Fore.RED +
            "Invalid choice. Please enter a number between 1 and 7." +
            colorama.Style.RESET_ALL
        )

    # Convert the user's menu choice into:
    # 1. An energy level name for display.
    # 2. An energy_level_id for future database storage.
    if energy_choice == "1":
        energy_level = "Drained"
    elif energy_choice == "2":
        energy_level = "Sluggish"
    elif energy_choice == "3":
        energy_level = "Mellow"
    elif energy_choice == "4":
        energy_level = "Steady"
    elif energy_choice == "5":
        energy_level = "Vibrant"
    elif energy_choice == "6":
        energy_level = "Driven"
    elif energy_choice == "7":
        energy_level = "Radiant"
    else:
        energy_level = "Unknown"

    # Ask whether the user has free time available today.
    # This information is used when generating recommendations.
    print(colorama.Fore.YELLOW + "\nDo you have free time today?" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "1. Yes" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "2. No" + colorama.Style.RESET_ALL)

    # Accept multiple valid responses such as:
    # 1, Yes, Y, 2, No, or N.
    while True:
        free_time_choice = input(
            colorama.Fore.LIGHTBLUE_EX +
            "Enter free time choice: " +
            colorama.Style.RESET_ALL
        ).lower()

        if free_time_choice in ["1", "yes", "y"]:
            free_time = True
            free_time_display = "Yes"
            break

        elif free_time_choice in ["2", "no", "n"]:
            free_time = False
            free_time_display = "No"
            break

        print(
            colorama.Fore.RED +
            "Invalid choice. Please enter Yes/No or 1/2." +
            colorama.Style.RESET_ALL
        )

    # Retrieve the user's current weather conditions using
    # the OpenWeather API. Continue prompting until a valid
    # city is entered and weather data is returned.
    while True:
        weather_result = get_user_input_for_weather()

        if weather_result:
            break

        print(
            colorama.Fore.RED +
            "Invalid city. Please try again." +
            colorama.Style.RESET_ALL
        )

    # Generate personalized recommendations using:
    # mood category, mood score, energy level,
    # free time availability, and weather conditions.
    recommendation_result = get_recommendations(
        mood_category,
        mood_score,
        energy_level,
        free_time,
        weather_result
    )

    # Display a summary of the journal entry so the user
    # can review all information before it is saved.
    print(
        colorama.Fore.CYAN +
        "\n---------- Journal Entry ------------" +
        colorama.Style.RESET_ALL
    )
    print(colorama.Fore.CYAN + f"Title: {title}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Content: {content}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Mood Category: {mood_category}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Mood Score: {mood_score}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Energy Level: {energy_level}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Free Time: {free_time_display}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Weather: {weather_result}" + colorama.Style.RESET_ALL)

    # Display the personalized recommendations generated
    # from the user's journal entry selections.
    print(
        colorama.Fore.GREEN +
        "\nRecommendations:" +
        colorama.Style.RESET_ALL
    )

    print(
        colorama.Fore.GREEN +
        recommendation_result +
        colorama.Style.RESET_ALL
    )

    journal_data = {
        "user_id": logged_in_id,
        "title": title,
        "content": content,
        "mood_category": int(mood_category_choice),
        "mood_score": int(mood_score_choice),
        "energy_level": int(energy_choice),
        "free_time": free_time,
        "weather": weather_result,
        "recommendations": recommendation_result
    }

    try:
        response = requests.post(
            f"{BASE_URL}/login/journal_entries",
            json=journal_data
        )

        if response.status_code != 201:
            print(colorama.Fore.RED +
                f"\nError: {response.text}" +
                colorama.Style.RESET_ALL)


    except requests.exceptions.RequestException as e:
        print(colorama.Fore.RED +
            f"\nConnection error: {e}" +
            colorama.Style.RESET_ALL)





def edit_journal_entry():

    # Display the Edit Journal Entry heading.
    print(
        colorama.Fore.CYAN +
        "\n========== EDIT JOURNAL ENTRY ==========" +
        colorama.Style.RESET_ALL
    )

    # TODO:
    # Replace this mock data with real journal entries from the database/API
    # once backend integration is ready.
    #
    # Currently this list is only used for testing the Console UI.
    journal_entries = [
        {
            "entry_id": 1,
            "title": "Test Entry 1",
            "content": "Today was a good day.",
            "mood_category": "Positive"
        },
        {
            "entry_id": 2,
            "title": "Test Entry 2",
            "content": "Feeling a bit tired today.",
            "mood_category": "Negative"
        }
    ]

    # Check whether any journal entries exist.
    # If the list is empty, notify the user and exit the function.
    if not journal_entries:
        print(
            colorama.Fore.RED +
            "\nNo journal entries found." +
            colorama.Style.RESET_ALL
        )
        return

    # Display all available journal entries so the user can
    # choose which entry they would like to edit.
    print(
        colorama.Fore.YELLOW +
        "\nAvailable journal entries:" +
        colorama.Style.RESET_ALL
    )

    for entry in journal_entries:
        print(
            colorama.Fore.CYAN +
            f"{entry['entry_id']}. {entry['title']} - Mood: {entry['mood_category']}" +
            colorama.Style.RESET_ALL
        )

    # Ask the user which journal entry they would like to edit.
    # Validation ensures the selected entry ID exists.
    while True:
        entry_choice = input(
            colorama.Fore.LIGHTBLUE_EX +
            "\nEnter the entry ID you want to edit: " +
            colorama.Style.RESET_ALL
        )

        # Check that the user entered a number.
        if entry_choice.isdigit():
            entry_choice = int(entry_choice)

            selected_entry = None

            # Search for the matching journal entry.
            for entry in journal_entries:
                if entry["entry_id"] == entry_choice:
                    selected_entry = entry
                    break

            # If a matching entry is found, continue.
            if selected_entry:
                break

        # Display an error message if the selected ID is invalid.
        print(
            colorama.Fore.RED +
            "Invalid entry ID. Please choose an entry from the list." +
            colorama.Style.RESET_ALL
        )

    # Display the current journal entry details before editing.
    # This allows the user to see the existing information.
    print(
        colorama.Fore.CYAN +
        "\nCurrent Entry Details:" +
        colorama.Style.RESET_ALL
    )

    print(
        colorama.Fore.CYAN +
        f"Title: {selected_entry['title']}" +
        colorama.Style.RESET_ALL
    )

    print(
        colorama.Fore.CYAN +
        f"Content: {selected_entry['content']}" +
        colorama.Style.RESET_ALL
    )

    # Ask the user for a new title.
    # Pressing Enter will keep the current title unchanged.
    new_title = input(
        colorama.Fore.LIGHTBLUE_EX +
        "\nEnter new title, or press Enter to keep current title: " +
        colorama.Style.RESET_ALL
    )

    # Ask the user for new journal content.
    # Pressing Enter will keep the current content unchanged.
    new_content = input(
        colorama.Fore.LIGHTBLUE_EX +
        "Enter new content, or press Enter to keep current content: " +
        colorama.Style.RESET_ALL
    )

    # Only update the title if the user entered a value.
    # Otherwise, keep the original title.
    if new_title.strip():
        selected_entry["title"] = new_title

    # Only update the content if the user entered a value.
    # Otherwise, keep the original content.
    if new_content.strip():
        selected_entry["content"] = new_content

    # Inform the user that the journal entry has been updated.
    print(
        colorama.Fore.GREEN +
        "\nJournal entry updated successfully." +
        colorama.Style.RESET_ALL
    )

    # Display the updated journal entry so the user can
    # confirm the changes have been applied correctly.
    print(
        colorama.Fore.CYAN +
        "\n---------- Updated Journal Entry ------------" +
        colorama.Style.RESET_ALL
    )

    print(
        colorama.Fore.CYAN +
        f"Entry ID: {selected_entry['entry_id']}" +
        colorama.Style.RESET_ALL
    )

    print(
        colorama.Fore.CYAN +
        f"Title: {selected_entry['title']}" +
        colorama.Style.RESET_ALL
    )

    print(
        colorama.Fore.CYAN +
        f"Content: {selected_entry['content']}" +
        colorama.Style.RESET_ALL
    )

    # TODO:
    # Replace the temporary update logic with an API/database update request.
    # Once integrated, changes will be permanently saved to the database
    # instead of being stored in temporary test data.



def delete_entry():
    # Display the Delete Journal Entry heading.
    print(
        colorama.Fore.CYAN +
        "\n========== DELETE JOURNAL ENTRY ==========" +
        colorama.Style.RESET_ALL
    )

    # TODO:
    # Replace this mock data with real journal entries from the database/API.
    # Currently this list is recreated every time the function runs,
    # so deleted entries will reappear when the program is restarted.
    journal_entries = [
        {
            "entry_id": 1,
            "title": "Test Entry 1",
            "content": "Today was a good day.",
            "mood_category": "Positive"
        },
        {
            "entry_id": 2,
            "title": "Test Entry 2",
            "content": "Feeling a bit tired today.",
            "mood_category": "Negative"
        }
    ]

    # Check if there are any journal entries available.
    # If the list is empty, inform the user and exit the function.
    if not journal_entries:
        print(
            colorama.Fore.RED +
            "\nNo journal entries found." +
            colorama.Style.RESET_ALL
        )
        return

    # Display all available journal entries so the user can
    # choose which one they would like to delete.
    print(
        colorama.Fore.YELLOW +
        "\nAvailable journal entries:" +
        colorama.Style.RESET_ALL
    )

    for entry in journal_entries:
        print(
            colorama.Fore.CYAN +
            f"{entry['entry_id']}. {entry['title']} - Mood: {entry['mood_category']}" +
            colorama.Style.RESET_ALL
        )

    # Ask the user which journal entry they would like to delete.
    # Validation ensures a valid entry ID is selected.
    while True:
        entry_choice = input(
            colorama.Fore.LIGHTBLUE_EX +
            "\nEnter the entry ID you want to delete: " +
            colorama.Style.RESET_ALL
        )

        # Check the user entered a number.
        if entry_choice.isdigit():
            entry_choice = int(entry_choice)

            selected_entry = None

            # Search through the journal entries to find
            # the entry matching the chosen ID.
            for entry in journal_entries:
                if entry["entry_id"] == entry_choice:
                    selected_entry = entry
                    break

            # If a matching entry was found, continue.
            if selected_entry:
                break

        # Display an error message if the entry ID does not exist.
        print(
            colorama.Fore.RED +
            "Invalid entry ID. Please choose an entry from the list." +
            colorama.Style.RESET_ALL
        )

    # Display the selected entry before deletion so the user
    # can confirm they have chosen the correct journal entry.
    print(colorama.Fore.CYAN + "\nSelected Entry:" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Entry ID: {selected_entry['entry_id']}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Title: {selected_entry['title']}" + colorama.Style.RESET_ALL)
    print(colorama.Fore.CYAN + f"Content: {selected_entry['content']}" + colorama.Style.RESET_ALL)

    # Ask the user to confirm whether they really want
    # to delete the selected journal entry.
    while True:
        confirm_delete = input(
            colorama.Fore.LIGHTBLUE_EX +
            "\nAre you sure you want to delete this entry? (Y/N): " +
            colorama.Style.RESET_ALL
        ).lower()

        # If the user confirms deletion,
        # remove the selected entry from the list.
        if confirm_delete in ["y", "yes"]:
            journal_entries.remove(selected_entry)

            print(
                colorama.Fore.GREEN +
                "\nJournal entry deleted successfully." +
                colorama.Style.RESET_ALL
            )
            break

        # If the user chooses not to delete,
        # leave the journal entry unchanged.
        elif confirm_delete in ["n", "no"]:
            print(
                colorama.Fore.YELLOW +
                "\nDelete cancelled. Journal entry was not deleted." +
                colorama.Style.RESET_ALL
            )
            break

        # Validation to ensure only Y or N responses are accepted.
        else:
            print(
                colorama.Fore.RED +
                "Invalid choice. Please enter Y or N." +
                colorama.Style.RESET_ALL
            )

    # TODO:
    # Replace journal_entries.remove() with an API/database delete request.
    # Once integrated, the journal entry will be permanently removed
    # from the database rather than from a temporary test list.

def search_entries(logged_in_id):

    print("=== Search Journal Entries ===")

    mood = input("Mood: ").strip()
    keyword = input("Keyword: ").strip()
    print("\nSort entries By:")
    print("1. Newest first")
    print("2. Oldest first")
    sort_choice = input("Your Choice (1/2): ").strip()


    if sort_choice == "2":
        sort = "date_asc"
    else:
        sort = "date_desc"

    limit = input("Number of entries to return (default 20): ").strip()

    params = {"user_id" : logged_in_id,
                 "sort" : sort
              }
    if limit:
        params["limit"] = limit

    if mood:
        params["mood"] = mood

    if keyword:
        params["keyword"] = keyword

    try:
        response = requests.get(
            f"{BASE_URL}/login/search_entries",
            params=params
        )

        data = response.json()

        if response.status_code != 200:
            print(data.get("error", "Unknown error"))
            return

        if not data["entries"]:
            print("No entries found.")
            return

        for entry in data["entries"]:

            print(f"Entry ID: {entry['entry_id']}")
            print(f"Title: {entry['title']}")
            print(f"Content: {entry['content']}")
            print(f"Mood Category: {entry['mood_category_id']}")
            print(f"Mood Score: {entry['mood_score_id']}")
            print(f"Energy Level: {entry['energy_level_id']}")
            print(f"Free Time: {entry['free_time']}")
            print(f"Weather: {entry['weather']}")
            print(f"Recommendations: {entry['recommendations']}")
            print(f"Created At: {entry['created_at']}")
            print("\n=================================")


    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")


def get_recommendations(category, mood, energy, free_time, weather):

        recommendations = []

        rainy_weather = ["Rain", "Drizzle", "Thunderstorm"]
        cloudy_weather = ["Clouds", "Mist"]
        cold_weather = ["Snow"]

        # NEGATIVE CATEGORY

        if category == "Negative":
            recommendations.append("Take a few minutes to reflect on what is causing stress.")
            recommendations.append("Practice deep breathing exercises.")

            if free_time:
                recommendations.append("Try a 10-minute guided meditation.")
                recommendations.append("Take a short walk to clear your mind.")

            if weather in rainy_weather:
                recommendations.append("Stay indoors and do relaxing activities.")

            elif weather in cloudy_weather:
                recommendations.append("A calm walk or indoor hobby would be nice.")

            elif weather in cold_weather:
                recommendations.append("Stay warm and have a hot drink.")

            else:
                recommendations.append("Good weather! Consider going outside.")

        # NEUTRAL CATEGORY

        elif category == "Neutral":
            recommendations.append("Try an enjoyable activity to boost your mood.")

            if free_time:
                recommendations.append("Read a book or listen to a podcast.")

            if weather == "Clear":
                recommendations.append("Consider taking a walk outside.")


        # POSITIVE CATEGORY

        elif category == "Positive":
            recommendations.append("Keep up the positive momentum.")
            recommendations.append("Celebrate today's achievements.")

            if free_time:
                recommendations.append("Spend time on a hobby you enjoy.")


        # AMBIGUOUS CATEGORY

        elif category == "Ambiguous":
            recommendations.append("Take some time to identify how you are feeling.")
            recommendations.append("Writing a journal entry may help clarify your thoughts.")

        # ENERGY LEVELS

        if energy in ["Drained", "Sluggish"]:
            recommendations.append("Prioritize rest and hydration.")
            recommendations.append("Avoid overcommitting yourself today.")

        elif energy in ["Driven", "Radiant"]:
            recommendations.append("Your energy is high. Consider exercise or a productive task.")

        # MOOD
        if mood == "Terrible":
            recommendations.append("Reach out to a trusted friend or family member.")

        elif mood == "Bad":
            recommendations.append("Focus on one small positive action today.")

        elif mood == "Fantastic":
            recommendations.append("Capture what's going well in your journal.")

        elif mood == "Mixed":
            recommendations.append("Acknowledge both positive and negative feelings.")

        elif mood == "Unsure":
            recommendations.append("Spend a few minutes reflecting on your emotions.")

        return "\n".join(f"• {item}" for item in recommendations)


def view_mood_summary(logged_in_id):

    try:
        response = requests.get(
            f"{BASE_URL}/login/mood_summary",
            params={"user_id": logged_in_id}
        )

        data = response.json()

        if response.status_code != 200:
            print(data.get("error", "Unknown error"))
            return

        summary = data["summary"]

        print("\n=================================")
        print("MOOD SUMMARY")
        print("=================================")

        print(f"Total Entries: {summary['total_entries']}")
        print(f"Positive: {summary['positive_entries']}")
        print(f"Neutral: {summary['neutral_entries']}")
        print(f"Negative: {summary['negative_entries']}")
        print(f"Ambiguous: {summary['ambiguous_entries']}")

        print(f"\nMost Common Mood: {data['most_common_mood']}")
        print(f"Average Mood Score: {summary['average_score_id']}")
        print(f"Average Energy: {summary['average_energy_id']}")

        print("\n=================================")

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")


# Function to interact with API
def run():

    # Print Main Menu
    print(colorama.Fore.BLUE +"\n WELCOME TO KindMind SYSTEM!!"+colorama.Style.RESET_ALL)
    # Alternatively to the console display, users can also be provided with the direct link to API for functions like view_journal_entry in login_menu() to view the data directly in API, like the below HomePage url(hardcoded in print statement).
    print(f"\nTo view KindMind API Home Page click: {BASE_URL}")
    print(colorama.Fore.YELLOW + "\na. To Register enter " + colorama.Fore.RED + " 1"+ colorama.Style.RESET_ALL)
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
        else:
            print("Invalid Input. Try Again!")



# Main function creates database first and then runs flask app to interact with API
if __name__ == "__main__":
    # 1. Create DB first (must complete before anything else)
    create_database()

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






