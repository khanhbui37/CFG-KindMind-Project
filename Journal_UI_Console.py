# IN PROGRESS
# ==================================================
# KindMind Console UI
# Journal Entry User Interaction Draft
#
# Purpose:
# Collect user journal information through
# a console-based interface.
#
# Features:
# - Title input
# - Journal content input
# - Mood category selection
# - Mood score selection
# - Energy level selection
# - Free time selection
# - Weather API integration still to be added
# - Validation still to be added
# ==================================================

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


# Keep this line only while testing this file by itself.
# Remove it when copying the function into main.py because the menu calls it there.
add_journal_entry()

