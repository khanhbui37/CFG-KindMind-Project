import mysql.connector
from config import db_config

# Helper function to connect to database
def get_connection():
    try:
        return mysql.connector.connect(**db_config)

    except mysql.connector.Error as error:
        print(f"Error: {error}")
        return None


def create_data_base():
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
                                             FOREIGN KEY (weather)
                                             REFERENCES weather_options(weather_id),
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