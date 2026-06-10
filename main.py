from app import app
import logging
import threading
import time
from db_utils import create_database, get_user_mood_summary, get_common_mood_category
import colorama
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
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

    # Perform user action
    while True:
        login_input = input(colorama.Fore.LIGHTBLUE_EX + "\nENTER YOUR CHOICE HERE: " + colorama.Style.RESET_ALL)

        if login_input == "1":
            add_journal_entry()
            break

        elif login_input == "2":
            view_journal_entry()
            break

        elif login_input == "3":
            edit_journal_entry()
            break

        elif login_input == "4":
            user_date = input("\nEnter date to search an entry (dd/mm/yyyy): ")

            try:
                search_date = datetime.strptime(user_date, "%d/%m/%Y")
                print("Valid date:", search_date.date())

                url_search_date = f"{BASE_URL}/journal_entries/{user_date}"

                response = requests.get(url_search_date)

                if response.status_code == 200:
                    data = response.json()  # Assuming API returns JSON
                    print("\nEntries found:")
                    print(data)
                elif response.status_code == 404:
                    print("No entries found for this date.")
                else:
                    print(f"Error: {response.status_code}")
                    print(response.text)

            except ValueError:
                print("Invalid date. Please use the format dd/mm/yyyy.")
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
            view_mood_summary()
            break

        elif login_input == "7":
            delete_entry()
            break

        elif login_input == "8":
            logout()
            break

        else:
            print("Invalid Input Please Try Again!")
            continue


def post_registration_info():
    pass

def view_journal_entry():
    pass

def add_journal_entry():
    pass

def edit_journal_entry():
    pass

def delete_entry():
    pass

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

def view_mood_summary():
    # Get summary data from database
    current_user_id = input("Please enter your user ID: ")

    summary = get_user_mood_summary(current_user_id)

    if not summary:
        print("No data found.")
        return

    most_common_mood = get_common_mood_category(current_user_id)

    print("\n=================================")
    print("MOOD SUMMARY")
    print("=================================")

    print(f"Total Entries: {summary['total_entries']}")
    print(f"Positive: {summary['positive_entries']}")
    print(f"Neutral: {summary['neutral_entries']}")
    print(f"Negative: {summary['negative_entries']}")
    print(f"Ambiguous: {summary['ambiguous_entries']}")

    print(f"\nMost Common Mood: {most_common_mood}")
    print(f"Average Mood Score: {summary['average_score_id']}")
    print(f"Average Energy: {summary['average_energy_id']}")

    print("\n=================================")

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






