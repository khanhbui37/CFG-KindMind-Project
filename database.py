"""
Experimental/reference file.

This file contains draft API/database ideas that may be merged or refactored later.
It is not currently aligned with the active KindMind app flow in main.py, app.py, db_utils.py,
or the cleaned kind_mind.sql schema.

Current active database schema:
- users
- mood_category
- mood_score
- energy_level
- journal_entries

Current journal_entries columns:
- entry_id
- user_id
- title
- content
- mood_category_id
- mood_score_id
- energy_level_id
- free_time
- weather
- recommendations
- created_at

This file may still contain older draft fields such as id, city, temperature,
weather_conditions, mood, and energy_level. These should be refactored before
being integrated into the active application.
"""

from datetime import date
import mysql.connector
import requests


from config_example import db_config
from flask import Flask, jsonify, request

from db_utils import insert_default_values, get_user_mood_summary, get_common_mood_category

app = Flask(__name__)


def run_simulation():
    print("   WELCOME TO KINDMIND    ")
    print("Initializing Database Connection...")
    print("Server starting on http://127.0.0.1:5001")
    print("Ready to process toy loans and inventory.\n")

if __name__ == "__main__":
    run_simulation()
    app.run(debug=True, port=5001)

@app.route('api/users', methods=['POST'])
def register_user():

    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Request body is missing or not valid JSON."}), 400

    name = data.get("Name")
    email = data.get("Email")
    hashed_password = data.get("Password")
    today_date = str(date.today())

    if not name or not email or not hashed_password:
        return jsonify({
            "error": "Missing required fields",
            "message": "Name, Email and Password are required to register."
        }), 400

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT User_id FROM Users WHERE Email = %s", (email,))
        if cursor.fetchone():
            return jsonify({
                "error": "Conflict",
                "message": f"An account with email '{email}' already exists."
            }), 409

        query = """
            INSERT INTO Users (Name, Email, Hashed_password, Created_at, Deleted_at) 
            VALUES (%s, %s, %s, %s, NULL)
        """
        cursor.execute(query, (name, email, hashed_password, today_date))
        db.commit()

        new_user_id = cursor.lastrowid

        return jsonify({
            "message": "User registered successfully.",
            "user": {
                "User_id": new_user_id,
                "Name": name,
                "Email": email,
                "Created_at": today_date
            }
        }), 201

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('api/users/<id>', methods=['DELETE'])
def delete_user(user_id):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM Users WHERE id = %s", (user_id,))
        db.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": f"User {user_id} deleted successfully!"}), 200

        return jsonify({"message": "Error, entry not found!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()
API_KEY = "os.getenv('WEATHER_API_KEY')"
API_URL = "https://api.openweathermap.org/data/2.5/weather"


@app.route('api/users/<id>', methods=['PUT'])
def create_journal(entry_id):
    data = request.get_json(force=True)
    if not data:
        return jsonify({"error": "Request body is missing or not valid JSON."}), 400

    city = data.get("City")
    temperature = None
    weather_conditions = None

    if city:
        try:
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric',
                'lang': 'pl'
            }
            response = requests.get(API_URL, params=params, timeout=5)

            if response.status_code == 200:
                weather_data = response.json()
                weather_conditions = weather_data['weather'][0]['description']
            else:
                return jsonify({"error": f"Error with data for: {city}. Please check city name."}), 400
        except Exception as e:
            return jsonify({"error": f"Error with connection with API: {str(e)}"}), 500

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM journal_entries WHERE id = %s", (entry_id,))
        entry = cursor.fetchone()

        today_date = data.get("Created At", str(date.today()))

        if entry:
            title = data.get("Title", entry["title"])
            content = data.get("Content", entry["content"])
            mood = data.get("Mood", entry["mood"])
            energy_level = data.get("Energy Level", entry["energy_level"])
            free_time = data.get("Free Time", entry["free_time"])
            city = city if city else entry.get("city")
            temperature = temperature if temperature is not None else entry.get("temperature")
            weather_conditions = weather_conditions if weather_conditions else entry.get("weather_conditions")

            query = """
                            UPDATE journal_entries 
                            SET title = %s, content = %s, mood = %s, energy_level = %s, free_time = %s,
                                city = %s, temperature = %s, weather_conditions = %s
                            WHERE id = %s
                        """
            cursor.execute(query, (title, content, mood, energy_level, free_time, city, temperature, weather_conditions,
                                   entry_id))
            db.commit()
            msg = "Journal entry updated successfully."
        else:
            title = data.get("Title", entry["title"])
            content = data.get("Content", entry["content"])
            mood = data.get("Mood", entry["mood"])
            energy_level = data.get("Energy Level", entry["energy_level"])
            free_time = data.get("Free Time", entry["free_time"])
            city = city if city else entry.get("city")
            temperature = temperature if temperature is not None else entry.get("temperature")
            weather_conditions = weather_conditions if weather_conditions else entry.get("weather_conditions")

            if not title or not content:
                return jsonify({"error": "Title and Content are required fields for creating a journal entry."}), 400

            query = """
                    INSERT INTO journal_entries (id, title, created_at, content, mood, energy_level, free_time,  city, temperature, weather_conditions) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
            cursor.execute(query,
                           (entry_id, title, content, mood, energy_level, free_time, today_date, city, temperature, weather_conditions))
            db.commit()
            msg = "Journal entry created successfully."

        return jsonify({
            "message": msg,
            "entry": {
                "id": entry_id,
                "Created At": str(today_date),
                "Title": title,
                "Content": content,
                "Mood": mood,
                "Energy Level": energy_level,
                "Free Time": free_time,
                "City": city,
                "Temperature": temperature,
                "Weather": weather_conditions
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500
    finally:
        cursor.close()
        db.close()


@app.route('api/users', methods=['GET'])
def get_all_journal_entries():
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM journal_entries")
        entries = cursor.fetchall()

        for entry in entries:
            if entry.get("created_at"):
                entry["created_at"] = str(entry["created_at"])

        return jsonify(entries), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()

@app.route('api/users', methods=['GET'])
def get_journal_entries_by_mood():
    target_mood = request.args.get('mood')

    if not target_mood:
        return jsonify({
            "error": "Missing query parameter",
            "message": "Please provide a mood parameter in the URL, for example: ?mood=Happy"
        }), 400

    db = mysql.connector.connect(**db_config)
    cursor = db.cursor(dictionary=True)

    try:
        query = "SELECT * FROM journal_entries WHERE mood = %s"
        cursor.execute(query, (target_mood,))
        entries = cursor.fetchall()

        for entry in entries:
            if entry.get("created_at"):
                entry["created_at"] = str(entry["created_at"])

        return jsonify({
            "status": "success",
            "searched_mood": target_mood,
            "count": len(entries),
            "data": entries
        }), 200

    except Exception as e:
        return jsonify({"error": "Database error", "details": str(e)}), 500
    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    app.run(debug=True, port=5001)

@app.route('api/users/<id>', methods=['DELETE'])
def delete_journal_entry(entry_id):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        cursor.execute("DELETE FROM journal_entries WHERE id = %s", (entry_id,))
        db.commit()

        if cursor.rowcount > 0:
            return jsonify({"message": f"Journal entry {entry_id} deleted successfully!"}), 200

        return jsonify({"message": "Error, entry not found!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        db.close()


"""
This part of code is option with Weather API. But to use it I think I need to change journal_entries table (adding city column) and probably delete weather options table. Please check and comment if I should make extra changes.
"""

# @app.route('/api/users', methods=['GET'])
# def get_journal_by_weather():
#     city = request.args.get('city')
#
#     if not city:
#         return jsonify(
#             {"error": "Missing query parameter", "message": "Please insert city name in format: ?city=CityName"}), 400
#
#     temperature, error = get_weather_condition(city)
#
#     if error:
#         return jsonify({"error": "Weather API Error", "details": error}), 502
#
#     if temperature >= 20:
#         weather_keyword = "Warm"
#     elif 10 <= temperature < 20:
#         weather_keyword = "Normal"
#     else:
#         weather_keyword = "Cold"
#
#     db = mysql.connector.connect(**db_config)
#     cursor = db.cursor(dictionary=True)
#
#     try:
#         query = """
#             SELECT * FROM journal_entries
#             WHERE content LIKE %s OR title LIKE %s OR mood LIKE %s
#         """
#         search_term = f"%{weather_keyword}%"
#         cursor.execute(query, (search_term, search_term, search_term))
#         entries = cursor.fetchall()
#
#         for entry in entries:
#             if entry.get("created_at"):
#                 entry["created_at"] = str(entry["created_at"])
#
#         return jsonify({
#             "status": "success",
#             "searched_city": city,
#             "current_temperature": f"{temperature}°C",
#             "weather_category": weather_keyword,
#             "matching_entries_count": len(entries),
#             "data": entries
#         }), 200
#
#     except Exception as e:
#         return jsonify({"error": "Database error", "details": str(e)}), 500
#     finally:
#         cursor.close()
#         db.close()
#
#
# if __name__ == "__main__":
#     app.run(debug=True, port=5001)