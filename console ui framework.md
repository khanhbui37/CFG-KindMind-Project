# KindMind Console UI Framework
# KindMind Python Console UI Framework

## Purpose

This document outlines the planned structure for the KindMind console-based user interface before implementation begins.

The console UI will allow users to navigate the application, manage journal entries, view recommendations, and access mood summaries.

---

## Main User Flow

Welcome Screen
↓
Register / Login
↓
Main Menu
↓
Choose Action
↓
Complete Action
↓
Return to Main Menu

---

## Welcome Menu

1. Register
2. Login
3. Exit

---

## Main Menu

1. Add Journal Entry
2. View Journal Entries
3. Edit Journal Entry
4. Delete Journal Entry
5. View Recommendations
6. Mood Summary
7. Logout
8. Exit

---

## Journal Entry Fields

When adding a journal entry, the user will be asked for:

- Title
- Journal content
- Mood
- Energy level
- Free time available

---

## Add Journal Entry Flow

1. User selects "Add Journal Entry"
2. System asks for title
3. System asks for journal content
4. System asks user to select mood
5. System asks user to select energy level
6. System asks if user has free time available
7. System validates input
8. System displays a summary of the entry
9. User confirms the entry
10. System returns to the main menu

---

## View Journal Entries Flow

1. User selects "View Journal Entries"
2. System displays all journal entries for the user
3. User can return to the main menu

---

## Edit Journal Entry Flow

1. User selects "Edit Journal Entry"
2. System displays available journal entries
3. User selects an entry to edit
4. User updates selected fields
5. System confirms the changes
6. System returns to the main menu

---

## Delete Journal Entry Flow

1. User selects "Delete Journal Entry"
2. System displays available journal entries
3. User selects an entry to delete
4. System asks for confirmation
5. Entry is deleted if confirmed
6. System returns to the main menu

---

## Proposed Functions

```python
show_welcome_menu()
show_main_menu()
register_user()
login_user()
add_journal_entry()
view_journal_entries()
edit_journal_entry()
delete_journal_entry()
view_recommendations()
view_mood_summary()
logout_user()
```

---

# 📊 Console UI Flowchart

The following diagram shows the planned navigation and user interaction flow for the KindMind console application.

![Console UI Flowchart](https://github.com/user-attachments/assets/07afa2eb-c8b9-4e23-9264-7b7f30e767cf)
