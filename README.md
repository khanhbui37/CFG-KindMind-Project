# 😌📔 KindMind - Wellbeing Journal System
####        Track your thoughts. Understand your moods. Improve your wellbeing.


---
## ℹ️ Project Info

This project was developed as part of the CFGDegree Software & Data Engineering Group Project.

## 📖 Project Overview

KindMind is a wellbeing journaling application designed to help users address mental overload and improve self-awareness. It enables users to record daily journal entries, track emotional patterns over time, and receive simple wellbeing insights. The app also provides personalized recommendations based on users’ mood trends and local weather conditions, helping them better understand their emotional wellbeing and build healthier habits.

### ✨ What can users do?

- 📝 Create journal entries
- 😊 Track mood, energy levels, and free time
- 🔍 Search and sort journal entries
- 💡 Receive recommendations based on mood and context
- 📊 View mood summaries and analytics

---

## 🚀 How to Use

1. 👤 Register a new account
2. 🔐 Log in using your credentials
3. 📝 Create a journal entry
4. 😊 Record your mood, energy level, and available free time
5. 💾 Save the entry
6. ✏️ View, edit, or delete previous entries
7. 🔍 Search and sort entries
8. 📊 View mood analytics and recommendations

---


## ✨ Features

### 👤 User Management

- User registration
- User login
- 🔒 Secure password hashing (specialisation topic ✅)

### 📝 Journal Management

- Create journal entries
- View journal entries
- Edit journal entries
- Delete journal entries

### 🔍 Search & Sort

- Search entries by keyword
- Filter entries by mood
- Sort entries by newest or oldest

### 🌤️ API Integration

- Weather-based wellbeing recommendations

### 📊 Analytics

- Mood frequency analysis
- Journaling activity summaries

---

## 🛠️ Technologies Used

- **Python** — core programming language
- **Flask** — web framework and REST API
- **MySQL** — database
- **Werkzeug** — secure password hashing
- **mysql-connector-python** — database connection
- **python-dotenv** — environment variable management
- **requests** — external API calls

 ---

## ⚙️ Installation & Setup

### Prerequisites

Make sure you have the following installed:
- Python 3.x — [download here](https://www.python.org/downloads/)
- MySQL — [download here](https://dev.mysql.com/downloads/)
- Git — [download here](https://git-scm.com/)

### 1. Clone the repository

```bash
git clone https://github.com/khanhbui37/CFG-KindMind-Project.git
cd CFG-KindMind-Project
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file in the root directory similar to the .env_example and add your API key:

```.env
WEATHER_API_KEY = YOUR_API_KEY_HERE
```

Open `.env` and update:

### 4. Configure Database

Create a `config.py` file in the root directory similar to the config_example.py and edit your details:

```config.py
db_config = {
    "host": "localhost",
    "user": "your_mysql_username",
    "password": "your_mysql_password"
}
```

---

## ▶️ Running the Application

### 1. Run the Flask File (app.py)
Run app.py using the command below and cnote down the port on which Flask is running in your system. If Flask is running on a port other than 5000, open main.py, update the BASE_URL variable, and set it to the Flask port being used on your system. If Flask is running on port 5000, no changes are required and you can proceed to the next step.

```bash
python app.py
```

### 5. Run the File Main.py

```bash
python main.py
```
This will:

1. Create the database (`kindMind`)
2. Start the Flask API
3. Launch the CLI interface where you can interact with API.

---

##  Database Structure

Database: `kindMind`

### Tables:

* **users**

  * user_id (Primary Key)
  * name
  * email
  * hashed_password
  * created_at

* **mood_category**

  * category_id (Primary Key)
  * category_name

* **mood_score**

  * score_id (Primary Key)
  * score_name

* **energy_level**

  * energy_id (Primary Key)
  * energy_name

* **journal_entries**

  * entry_id (Primary Key)
  * user_id  (Foreign Key)
  * title
  * content
  * mood_category_id (Foreign Key)
  * mood_score_id (Foreign Key)
  * energy_level_id (Foreign Key)
  * free_time
  * weather
  * recommendations
  * created_at

---

### Links To API Endpoints:

* Home Page (GET):
  http://127.0.0.1:5000/

* Register New User (POST):
  http://127.0.0.1:5000/register

* User Login (Method:POST):
  http://127.0.0.1:5000/login

* Add Journal Entries (Method:POST):
  http://127.0.0.1:5000/login/journal_entries

* View Journal Entries (Method:GET):
  http://127.0.0.1:5000/login/journal_entries/<int:entry_id>

* Edit Journal Entries (Method:PUT):
  http://127.0.0.1:5000/login/journal_entries/<int:entry_id>

* Search/Filter Journal Entries (Method:GET):
  http://127.0.0.1:5000/login/search_entries

* View Mood Summary (Method:GET):
  http://127.0.0.1:5000/login/mood_summary

* Delete Journal Entries (Method:DELETE):
  http://127.0.0.1:5000/login/journal_entries/<int:entry_id>


---

## 🧪 Testing Approach

KindMind does not follow strict Test-Driven Development. The main application features were built first, and tests were added afterwards to check existing functionality, support debugging, and reduce the risk of breaking working features during integration.

Our testing approach is best described as **post-development regression testing**, using a combination of:

* unit testing
* integration testing
* mock-based database testing
* manual end-to-end testing

> **Note:** This project uses a post-development testing approach rather than strict Test-Driven Development. Automated tests were added after the main features were implemented, with a focus on checking existing functionality, supporting integration work, and reducing the risk of regressions. Manual testing was also used for the console-based user journey in `main.py`, as some user input/output flows were better checked manually within the project timeframe.

---

### Automated Testing

Automated tests were added for key parts of the project after the core functionality was developed.

The database utility tests focus on checking the behaviour of functions in `db_utils.py`. These tests use mocked database connections and cursors, so they can run without needing a live MySQL database. This makes the tests safer to run across different local environments and avoids changing real project data during testing.

The integration tests focus on checking how the Flask routes behave when they receive requests. These tests help confirm that important routes return the expected status codes, response messages and data structures.

Automated testing covers areas such as:

* database connection handling
* database and table creation logic
* user creation
* password hashing behaviour
* journal entry creation
* viewing journal entries
* updating journal entries
* deleting journal entries
* retrieving the logged-in user ID
* searching journal entries
* mood summary helper logic
* registration behaviour
* login behaviour

---

### Manual Testing

Manual testing was also used because the project includes a console-based user interface in `main.py`. Some console interactions are harder to test automatically within the available project time, so the main user journey was checked manually.

Manual testing focused on:

* starting the application successfully
* registering a new user
* preventing duplicate email registration
* logging in with valid credentials
* rejecting incorrect login details
* adding a journal entry
* viewing journal entries
* editing a journal entry
* deleting a journal entry
* searching journal entries
* viewing the mood summary
* checking that console error messages are clear and do not return `None`

---

### Running the Tests

To run the tests, make sure the project dependencies are installed first:

```bash
pip install -r requirements.txt
```

Then run the database utility tests:

```bash
python -m pytest test_db_utils.py -v
```

To run the integration tests:

```bash
python -m pytest test_kindmind_integration.py -v
```

To run all available tests:

```bash
python -m pytest -v
```

Using `python -m pytest` is recommended because it is more reliable across different local Python environments, especially on Windows.

---

### Testing Limitations

Due to time constraints, we did not create separate dedicated `test_app.py` and `test_main.py` files.

Instead:

* Flask route behaviour is covered through the integration tests
* database behaviour is covered through `db_utils.py` tests
* console behaviour in `main.py` is checked through manual testing

This means the project does not have complete automated test coverage for every file. However, the combination of automated tests and manual testing gives coverage of the main user flows and the most important database and route behaviours.

---

### Future Testing Improvements

If more time were available, useful future testing improvements would include:

* adding a dedicated `test_main.py` file for console input/output behaviour
* adding a dedicated `test_app.py` file for more detailed Flask route testing
* expanding integration tests for more edge cases
* adding more tests after the OOP changes in `app.py`
* adding coverage reporting with `pytest-cov`
* adding automated tests for weather API failure handling
* adding tests for database casing consistency across local environments

---

## 👥 Team Members

- Hayley Selcraig
- Aamna Khan
- Amegna Mohankumar
- Ruth Touloum
- Khanh Bui Phuong
- Magdalena Zdunek
- Ayesha Grewal

---
## Project Activity Log

Please use this [link](https://docs.google.com/spreadsheets/d/1UK1Sqdbwy7oSx5mjZLknlmH0eKskx8uv/edit?gid=2037823253#gid=2037823253) to access our Activity Log. 