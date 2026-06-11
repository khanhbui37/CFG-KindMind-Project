from app import app
import logging
import threading
import time
from db_utils import create_data_base
import colorama
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

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={current_city}&appid={api_key}&units=metric"
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
    city = input("\nEnter your city to check the weather: ")

    weather = get_current_weather(city)

    return weather


def generate_recommendations(category, mood, energy, free_time, weather):
    recommendations = []

    rainy_weather = ["Rain", "Drizzle", "Thunderstorm"]
    cloudy_weather = ["Clouds", "Mist"]
    cold_weather = ["Snow"]

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

    elif category == "Neutral":
        recommendations.append("Try an enjoyable activity to boost your mood.")

        if free_time:
            recommendations.append("Read a book or listen to a podcast.")

        if weather == "Clear":
            recommendations.append("Consider taking a walk outside.")

    elif category == "Positive":
        recommendations.append("Keep up the positive momentum.")
        recommendations.append("Celebrate today's achievements.")

        if free_time:
            recommendations.append("Spend time on a hobby you enjoy.")

    elif category == "Ambiguous":
        recommendations.append("Take some time to identify how you are feeling.")
        recommendations.append("Writing a journal entry may help clarify your thoughts.")

    if energy in ["Drained", "Sluggish"]:
        recommendations.append("Prioritise rest and hydration.")
        recommendations.append("Avoid overcommitting yourself today.")

    elif energy in ["Driven", "Radiant"]:
        recommendations.append("Your energy is high. Consider exercise or a productive task.")

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
    print(colorama.Fore.RED + "\nADD JOURNAL ENTRY" + colorama.Style.RESET_ALL)

    # Ask the user for the journal title and main journal content.
    # This information will eventually be stored in the journal_entries table.
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

    # Display the mood categories available to the user.
    # These options match the values stored in the mood_category table.
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

        if mood_category_choice in ["1", "2", "3", "4"]:
            break

        print(
            colorama.Fore.RED +
            "Invalid choice. Please enter a number between 1 and 4." +
            colorama.Style.RESET_ALL
        )

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

    while True:
        mood_score_choice = input(
            colorama.Fore.LIGHTBLUE_EX +
            "Enter mood score choice: " +
            colorama.Style.RESET_ALL
        )

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
    print(colorama.Fore.YELLOW + "\nChoose your energy level:" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "1. Drained" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "2. Sluggish" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "3. Mellow" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "4. Steady" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "5. Vibrant" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "6. Driven" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "7. Radiant" + colorama.Style.RESET_ALL)

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

    print(colorama.Fore.YELLOW + "\nDo you have free time today?" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "1. Yes" + colorama.Style.RESET_ALL)
    print(colorama.Fore.YELLOW + "2. No" + colorama.Style.RESET_ALL)

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

    # Get weather from the weather API.
    while True:
        weather_result = get_user_input_for_weather()

        if weather_result:
            break

        print(
            colorama.Fore.RED +
            "Invalid city. Please try again." +
            colorama.Style.RESET_ALL
        )

    # Generate recommendations based on the user's journal choices.
    # This recommendation text will later be stored in the journal_entries table.
    recommendation_result = generate_recommendations(
        mood_category,
        mood_score,
        energy_level,
        free_time,
        weather_result
    )

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

    print(
        colorama.Fore.GREEN +
        "\nJournal entry created successfully." +
        colorama.Style.RESET_ALL
    )

    # TODO:
    # Send the collected data to the API/database once integration is complete.
    # Data to be stored includes:
    # title
    # content
    # mood_category_id
    # mood_score_id
    # energy_level_id
    # free_time
    # weather_result
    # recommendation_result

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






