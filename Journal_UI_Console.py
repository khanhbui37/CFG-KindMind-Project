IN PROGRESS
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
# - Mood selection
# - Validation (coming next)
# ==================================================

def add_journal_entry():
    print("Add journal entry")

    title = input ("Enter a title: ")
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

add_journal_entry()
