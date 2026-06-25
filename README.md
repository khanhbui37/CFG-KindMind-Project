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

* Search/Filter Journal Entries (Method:GET):
  http://127.0.0.1:5000/login/search_entries

* View Mood Summary (Method:GET):
  http://127.0.0.1:5000/login/mood_summary

* Delete Journal Entries (Method:DELETE):
  http://127.0.0.1:5000/login/journal_entries/<int:entry_id>


---

## 🧪 Testing

*To be confirmed*

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
