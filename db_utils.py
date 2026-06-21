import mysql.connector
from config_example import db_config

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
        cursor.execute("CREATE DATABASE IF NOT EXISTS KindMind")
        cursor.execute("USE KindMind")

        tables = {
            "users": """ CREATE TABLE IF NOT EXISTS users (
                                             user_id INT PRIMARY KEY AUTO_INCREMENT,
                                             name VARCHAR(100) NOT NULL,
                                             email VARCHAR(100) UNIQUE NOT NULL,
                                             hashed_password VARCHAR(255) NOT NULL,
                                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""",
            "mood_category": """ CREATE TABLE IF NOT EXISTS mood_category (
                                             category_id  INT PRIMARY KEY AUTO_INCREMENT,
                                             category_name VARCHAR(100) UNIQUE NOT NULL)""",
            "mood_score": """ CREATE TABLE IF NOT EXISTS mood_score(
                                             score_id INT PRIMARY KEY AUTO_INCREMENT,
                                             score_name VARCHAR(100) UNIQUE NOT NULL)""",
            "energy_level": """ CREATE TABLE IF NOT EXISTS energy_level (
                                             energy_id INT PRIMARY KEY AUTO_INCREMENT,
                                             energy_name VARCHAR(100) UNIQUE NOT NULL)""",
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
                                             energy_level_id INT NOT NULL,
                                             FOREIGN KEY (energy_level_id)
                                             REFERENCES energy_level(energy_id),
                                             free_time BOOLEAN NOT NULL,
                                             weather VARCHAR(50) NOT NULL,
                                             recommendations TEXT,
                                             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL)"""

        }

        try:
            for name, query in tables.items():
                cursor.execute(query)

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


def create_user(data):

    db = None
    cursor = None

    try:
        db = get_connection()  # connect to database
        cursor = db.cursor()


        query = """
            INSERT INTO users
            (name, email, hashed_password)
            VALUES (%s, %s, %s)
            """

        values = (
            data["name"],
            data["email"],
            data["password"]
        )

        cursor.execute("""USE KindMind""")
        cursor.execute(query, values)

        db.commit()

        return {"message":"User Successfully Added"}

    except mysql.connector.IntegrityError as err:
        return {"error": f"Integrity error: {err}"}

    except mysql.connector.DataError as err:
        return {"error": f"Invalid data: {err}"}

    except mysql.connector.ProgrammingError as err:
        return {"error": f"SQL error: {err}"}

    except mysql.connector.OperationalError as err:
        return {"error": f"Connection issue: {err}"}

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

def create_journal_entry(data):

    db = None
    cursor = None

    try:
        db = get_connection()  # connect to database
        cursor = db.cursor()

        query = """
            INSERT INTO journal_entries
            (user_id, title, content, mood_category_id, mood_score_id, energy_level_id,
            free_time, weather, recommendations)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

        values = (
            data["user_id"],
            data["title"],
            data["content"],
            data["mood_category"],
            data["mood_score"],
            data["energy_level"],
            data["free_time"],
            data["weather"],
            data["recommendations"]
        )

        cursor.execute("""USE KindMind""")
        cursor.execute(query, values)

        db.commit()

        return {"message":"Journal Entry Successfully Added"}

    except mysql.connector.IntegrityError as err:
        return {"error": f"Integrity error: {err}"}

    except mysql.connector.DataError as err:
        return {"error": f"Invalid data: {err}"}

    except mysql.connector.ProgrammingError as err:
        return {"error": f"SQL error: {err}"}

    except mysql.connector.OperationalError as err:
        return {"error": f"Connection issue: {err}"}

    except mysql.connector.Error as err:
        return {"error": f"Database error: {err}"}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def get_logged_in_user_id(user_email):
    db = None
    cursor = None
    logged_info = None

    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        query = """
            SELECT user_id FROM users 
            WHERE email = %s"""

        cursor.execute("USE KindMind")
        cursor.execute(query, (user_email,))
        logged_info = cursor.fetchone()

    except mysql.connector.Error as error:
        print(f"Something went wrong: {error}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return logged_info["user_id"] if logged_info else None



def get_searched_entries(user_id, mood, keyword, sort, limit):
    db = None
    cursor = None
    entries = None

    try:
        db = get_connection()
        cursor = db.cursor(dictionary=True)

        query = """
                SELECT *
                FROM journal_entries
                WHERE user_id = %s
            """

        params = [user_id]

        if mood:
            query += " AND mood_category_id = %s"
            params.append(mood)

        if keyword:
            query += """
                    AND (
                        title LIKE %s
                        OR content LIKE %s
                    )
                """
            search_term = f"%{keyword}%"
            params.extend([search_term, search_term])


        if sort == "date_asc":
            query += " ORDER BY created_at ASC"
        else:
            query += " ORDER BY created_at DESC"

        query += " LIMIT %s"
        params.append(limit)

        cursor.execute("USE KindMind")
        cursor.execute(query, params)
        entries = cursor.fetchall()


    except mysql.connector.Error as error:
        print(f"Something went wrong: {error}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return entries if entries else None



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
            JOIN energy_level el ON je.energy_level_id = el.energy_id
    
        WHERE user_id = %s
        GROUP BY user_id
        """

        cursor.execute("USE KindMind")
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
    common_category = None

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

        cursor.execute("USE KindMind")
        cursor.execute(query, (user_id,))
        common_category = cursor.fetchone()

    except mysql.connector.Error as error:
        print(f"Something went wrong: {error}")

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return common_category["category_name"] if common_category else None

# Backwards-compatible alias for existing tests branch naming (test_kindmind.py)
def create_data_base():
    return create_database()
