IN PROGRESS

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
