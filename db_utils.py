import mysql.connector
from config import db_config

# Helper function to connect to database
def get_connection():
    try:
        return mysql.connector.connect(**db_config)

    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return None


def create_database():
    db = None
    cursor = None

    try:
        db = get_connection()  # connect to database
        cursor = db.cursor()

        # create database and tables if not exists before
        cursor.execute("CREATE DATABASE IF NOT EXISTS kindMind")
        cursor.execute("USE kindMind")

        tables = {
            "users": """ CREATE TABLE IF NOT EXISTS users (
                                             user_id INT PRIMARY KEY AUTO_INCREMENT,
                                             name VARCHAR(100) NOT NULL,
                                             email VARCHAR(100) UNIQUE NOT NULL,
                                             hashed_password VARCHAR(255) NOT NULL,
                                             created_at DATE NOT NULL)""",
            "mood_category": """ CREATE TABLE IF NOT EXISTS mood_category (
                                             category_id  INT PRIMARY KEY AUTO_INCREMENT,
                                             category_name VARCHAR(100) UNIQUE NOT NULL)""",
            "mood_score": """ CREATE TABLE IF NOT EXISTS mood_score(
                                             score_id INT PRIMARY KEY AUTO_INCREMENT,
                                             score_name VARCHAR(100) UNIQUE NOT NULL)""",
            "energy_level": """ CREATE TABLE IF NOT EXISTS energy_level (
                                             energy_id INT PRIMARY KEY AUTO_INCREMENT,
                                             energy_name VARCHAR(100) UNIQUE NOT NULL)""",
            "weather_options": """ CREATE TABLE IF NOT EXISTS weather_options (
                                             weather_id INT PRIMARY KEY AUTO_INCREMENT,
                                             weather_name VARCHAR (100) UNIQUE NOT NULL)""",
            "journal_entries": """ CREATE TABLE IF NOT EXISTS journal_entries (
                                             entry_id INT PRIMARY KEY AUTO_INCREMENT,
                                             user_id INT NOT NULL, 
                                             FOREIGN KEY (user_id)
                                             REFERENCES users(user_id) ON DELETE CASCADE,
                                             title VARCHAR(100) NOT NULL,
                                             content TEXT NOT NULL,
                                             mood_category_id INT NOT NULL,
                                             FOREIGN KEY (mood_category_id)
                                             REFERENCES mood_category(category_id),
                                             mood_score_id INT NOT NULL,
                                             FOREIGN KEY (mood_score_id)
                                             REFERENCES mood_score(score_id),
                                             energy_level INT NOT NULL,
                                             FOREIGN KEY (energy_level)
                                             REFERENCES energy_level(energy_id),
                                             free_time BOOLEAN NOT NULL,
                                             weather INT NOT NULL,
                                             recommendations TEXT,
                                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)"""

        }

        try:
            for name, query in tables.items():
                cursor.execute(query)
                print(f"Created table {name}")

        except mysql.connector.Error as error:
            print(f"Error creating table: {error}")


        # Insert default values
        insert_default_values(cursor)

        db.commit()

    except mysql.connector.Error as error:
        print(f"Something went wrong:{error}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def insert_default_values(cursor):

    # Mood Categories
    cursor.executemany(
        """
        INSERT IGNORE INTO mood_category (category_name)
        VALUES (%s)
        """,
        [
            ('Negative',),
            ('Neutral',),
            ('Positive',),
            ('Ambiguous',)
        ]
    )

    # Mood Scores
    cursor.executemany(
        """
        INSERT IGNORE INTO mood_score (score_name)
        VALUES (%s)
        """,
        [
            ('Terrible',),
            ('Bad',),
            ('Off',),
            ('Ok',),
            ('Good',),
            ('Great',),
            ('Fantastic',),
            ('Mixed',),
            ('Unsure',)
        ]
    )

    # Energy Level
    cursor.executemany(
        """
        INSERT IGNORE INTO energy_level (energy_name)
        VALUES (%s)
        """,
        [
            ('Drained',),
            ('Sluggish',),
            ('Mellow',),
            ('Steady',),
            ('Vibrant',),
            ('Driven',),
            ('Radiant',)
        ]
    )

    # Weather Options
    cursor.executemany(
        """
        INSERT IGNORE INTO weather_options (weather_name)
        VALUES (%s)
        """,
        [
            ('Sunny',),
            ('Mostly Sunny',),
            ('Hot & Scorching',),
            ('Partly Cloudy',),
            ('Mostly Cloudy',),
            ('Overcast',),
            ('Light Drizzle',),
            ('Showers',),
            ('Heavy Rain',),
            ('Light Snow',),
            ('Heavy Snow',),
            ('Freezing Rain',),
            ('Thunderstorm',),
            ('Windy',),
            ('Foggy / Misty',)
        ]
    )

def get_user_mood_summary(user_id):
    db = None
    cursor = None
    summary = None

    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        query = """
        SELECT
            user_id,
            COUNT(entry_id) AS total_entries,
            ROUND(AVG(score_id), 2) AS average_score_id,
            ROUND(AVG(energy_id), 2) AS average_energy_id,

            SUM(CASE WHEN category_name = 'Positive' THEN 1 ELSE 0 END) AS positive_entries,
            SUM(CASE WHEN category_name = 'Neutral' THEN 1 ELSE 0 END) AS neutral_entries,
            SUM(CASE WHEN category_name = 'Negative' THEN 1 ELSE 0 END) AS negative_entries,
            SUM(CASE WHEN category_name = 'Ambiguous' THEN 1 ELSE 0 END) AS ambiguous_entries,

            MAX(created_at) AS latest_entry,

            CASE
                WHEN AVG(score_id) <= 3 AND AVG(energy_id) <= 2
                    THEN 'Gentle support may be helpful.'
                WHEN SUM(CASE WHEN category_name = 'Negative' THEN 1 ELSE 0 END) >= 3
                    THEN 'Several challenging check-ins logged.'
                WHEN AVG(score_id) >= 5
                    THEN 'Mostly positive pattern in this sample.'
                ELSE 'Mixed or steady mood pattern.'
            END AS supportive_summary

        FROM journal_entries je
            JOIN mood_category mc ON je.mood_category_id = mc.category_id
            JOIN mood_score ms ON je.mood_score_id = ms.score_id
            JOIN energy_level el ON je.energy_level = el.energy_id
    
        WHERE user_id = %s
        GROUP BY user_id
        """

        cursor.execute("USE kindMind")
        cursor.execute(query, (user_id,))
        summary = cursor.fetchone()

    except mysql.connector.Error as error:
        print(f"Something went wrong: {error}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return summary if summary else None

def get_common_mood_category(user_id):
    db = None
    cursor = None
    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        query = """
        SELECT category_name, COUNT(*) AS count
        
        FROM journal_entries je
        JOIN mood_category mc ON je.mood_category_id = mc.category_id
        
        WHERE user_id = %s
        GROUP BY category_name
        ORDER BY count DESC
        LIMIT 1"""

        cursor.execute("USE kindMind")
        cursor.execute(query, (user_id,))
        common_category = cursor.fetchone()

        return common_category["category_name"] if common_category else None

    except mysql.connector.Error as error:
        print(f"Something went wrong: {error}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
