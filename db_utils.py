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
                                             id INT PRIMARY KEY AUTO_INCREMENT,,
                                             name VARCHAR(100) NOT NULL,
                                             email VARCHAR(100) UNIQUE NOT NULL,
                                             Hashed_password VARCHAR(255) NOT NULL,
                                             Created_at DATE NOT NULL)""",
            "mood_category": """ CREATE TABLE IF NOT EXISTS mood_category (
                                             id INT PRIMARY KEY AUTO_INCREMENT,
                                             name VARCHAR(100) NOT NULL)"""


        # @Magdalena I have created 2 tables for your reference, you can create the remaining tables here in the same format. As we have to follow naming conventions I have kept the first letter of variable names in lowercase and as you have created variables within the respective tables, instead of using table names for variables like "user_id", just "id" would be enough.

        #After creating tables, it needs to be checked for if the table is empty, only if the table is empty, you can insert the values into the table(same values which you have in your branch)

        }

        for name, query in tables.items():
            cursor.execute(query)
            print(f"Created table {name}")

        db.commit()

    except mysql.connector.Error as error:
        print(f"Something went wrong:{error}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

#