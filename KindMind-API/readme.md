# KindMind API Log
====================
**Newest version in App1.py**
## How to set up the API
1. Open the project folder in your terminal.
2. Create and activate a virtual environment:
   - Windows: `python -m venv .venv` then `.venv\Scripts\activate`
3. Install the required packages:
   - `pip install flask`
4. Run the API locally:
   - `App.py`
5. Test the endpoints using Postman, cursor or your browser.

## Objectives
(Open Weather API)
What will the app do?

- [x] Allow users to register, log in securely and access their own journal data.
- [x] Allow users to create, view, edit and delete journal entries stored in MySQL.
- [x] Record mood, energy level, free time, timestamp and optional weather data with each entry.
- [x] Allow users to search entries by keyword, filter by mood and sort entries by date.
- [x] Use a Weather API to store weather conditions alongside journal entries.
- [ ] Generate simple rule-based recommendations based on mood, energy, time available and weather.
- [ ] Show basic analytics such as most common mood, entries per mood and journaling frequency.



## What has been done so far?
1. Created registration and verification so usernames are not duplicated in the database and new accounts can be created successfully. (04/06/2026)
2. Started implementing password hashing for secure login preparation. (06/06/2026)
3. Set up the basic journal API structure for creating and updating journal entries. (11/06/2026)
4. Deleted duplicate update endpoint, unified weather data (the weather code is based on api mapping)

## Next steps
1. Complete the login endpoint and finish secure password hashing and verification.
2. Build the recommendation section using rule-based suggestions based on mood, energy, time available and weather.
3. Create analytics based on the user's journal inputs.
4. connect dbutils 
5. error handling 

**PLEASE OVERVIEW THIS CODE THROUGHLY AND SUGGEST IMPROVEMENT**