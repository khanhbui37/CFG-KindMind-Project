from flask import Flask, jsonify, request
from db_utils import (
    get_connection,
    get_user_mood_summary,
    get_common_mood_category,
    create_user,
    create_journal_entry,
    get_searched_entries,
    get_user_journal_entries,
    update_journal_entry,
    delete_journal_entry,
    get_logged_in_user_id
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import re
import mysql.connector

app = Flask(__name__)

# OOP Models 

class User:
    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password,password)
    

class JournalEntry:
    def __init__(self, title, content, mood, energy_level):
        self.title = title
        self.content = content
        self.mood = mood
        self.energy_level = energy_level
    
    def get_summary(self):
        return f"'{self.title}' - Mood: {self.mood}, Energy: {self.energy_level}/10"

# user created entries
entry_a = JournalEntry("Monday", "Had a fantastic day!", "happy", 9)
entry_b = JournalEntry("Tuesday", "Felt tired", "calm", 4)

# Use them
print(f"entry_a: {entry_a.get_summary()}")
print(f"entry_b: {entry_b.get_summary()}")
print(f"entry_a mood: {entry_a.mood}")
print(f"entry_b mood: {entry_b.mood}")


# Hash password before saving it to the database.
def hash_password(password):
    return generate_password_hash(password)

# Check typed password against the stored password hash.
def verify_password(stored_hash, password):
    return check_password_hash(stored_hash, password)

# Helper function to validate user info.
def validate_user_fields(data):

    errors = []

    # Get user registration fields from the request body.
    # Default to an empty string so validation does not crash if a field is missing.
    user_name = data.get("name", "")
    user_email = data.get("email", "")
    user_password = data.get("password", "")

    # Name validation
    if not isinstance(user_name, str) or not user_name.strip():
        errors.append("Name cannot be empty.")

    elif len(user_name.strip()) < 2:
        errors.append("Name must be at least 2 characters.")

    elif not re.match(r"^[A-Za-z ]+$", user_name):
        errors.append("Name can only contain letters and spaces.")

    # Email validation
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not isinstance(user_email, str) or not re.match(pattern, user_email):
        errors.append("Invalid email format.")

    # Password validation
    if not isinstance(user_password, str) or len(user_password) < 7:
        errors.append("Password must be at least 7 characters.")

    elif not re.search(r"[A-Z]", user_password):
        errors.append("Password must contain an uppercase letter.")

    elif not re.search(r"[a-z]", user_password):
        errors.append("Password must contain a lowercase letter.")

    elif not re.search(r"\d", user_password):
        errors.append("Password must contain a number.")

    elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", user_password):
        errors.append("Password must contain a special character.")

    # If basic validation has already failed, return before checking the database.
    if errors:
        return errors

    # Checks if email exists already.
    db = None
    cursor = None

    try:
        db = get_connection()

        if db is None:
            return {"error": "Database connection failed."}

        cursor = db.cursor()

        cursor.execute("""USE KindMind""")
        cursor.execute("SELECT * FROM users WHERE email = %s", (user_email,))
        result = cursor.fetchone()

        if result:
            errors.append("Email already exists. Please Login with your email.")

    except mysql.connector.OperationalError as e:
        return {"error": f"Database connection issue: {e}"}

    except mysql.connector.ProgrammingError as e:
        return {"error": f"SQL error: {e}"}

    except mysql.connector.Error as e:
        return {"error": f"MySQL error: {e}"}

    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return errors if errors else None

# Helper function to validate login info.
def validate_login_data(data):
    errors = []

    # Get login fields from the request body.
    user_password = data.get("password", "")
    user_email = data.get("email", "")

    # Email and password must both be strings.
    if not isinstance(user_email, str) or not isinstance(user_password, str):
        errors.append("Email and password are required.")
        return errors

    # Email and password cannot be empty.
    if not user_email.strip() or not user_password:
        errors.append("Email and password are required.")
        return errors

    # Email validation
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, user_email):
        errors.append("Invalid email format.")

    # Password validation
    if len(user_password) < 7:
        errors.append("Password must be at least 7 characters.")

    elif not re.search(r"[A-Z]", user_password):
        errors.append("Password must contain an uppercase letter.")

    elif not re.search(r"[a-z]", user_password):
        errors.append("Password must contain a lowercase letter.")

    elif not re.search(r"\d", user_password):
        errors.append("Password must contain a number.")

    elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", user_password):
        errors.append("Password must contain a special character.")

    # If validation has failed, return before checking the database.
    if errors:
        return errors

    # Verify login details against database.
    db = None
    cursor = None

    try:
        db = get_connection()

        if db is None:
            return {"error": "Database connection failed."}

        cursor = db.cursor(dictionary=True)

        cursor.execute("""USE KindMind""")

        query = """
        SELECT user_id, email, hashed_password
        FROM users
        WHERE email = %s
        """

        cursor.execute(query, (user_email,))
        user = cursor.fetchone()

        if not user:
            errors.append("Email and password do not match.")

        elif not verify_password(user["hashed_password"], user_password):
            errors.append("Email and password do not match.")

    except mysql.connector.OperationalError as e:
        return {"error": f"Database connection issue: {e}"}

    except mysql.connector.ProgrammingError as e:
        return {"error": f"SQL error: {e}"}

    except mysql.connector.Error as e:
        return {"error": f"MySQL error: {e}"}

    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return errors if errors else None


# Helper Function to validate add journal entry details
def validate_add_journal_entry(data):

    errors=[]

    # Extract fields.
    user_id = data.get("user_id")
    title = data.get("title")
    content = data.get("content")
    mood_category = data.get("mood_category")
    mood_score = data.get("mood_score")
    energy_level = data.get("energy_level")
    free_time = data.get("free_time")
    weather = data.get("weather")
    recommendations = data.get("recommendations")

    # Validate user_id.
    if user_id is None:
        errors.append("User ID is required")

    if not isinstance(user_id, int):
        errors.append("User ID must be an integer.")

    # Validate title.
    if not isinstance(title, str) or not title.strip():
        errors.append("Title is required.")

    elif len(title.strip()) > 100:
        errors.append("Title cannot exceed 100 characters.")

    # Validate content.
    if not isinstance(content, str) or not content.strip():
        errors.append("Content is required.")

    elif len(content) > 5000:
        errors.append("Content cannot exceed 5000 characters.")

    # Validate mood category.
    if mood_category not in [1, 2, 3, 4]:
        errors.append("Invalid mood category.")

    # Validate mood score.
    if mood_score not in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        errors.append("Invalid mood score.")

    # Validate energy level.
    if energy_level not in [1, 2, 3, 4, 5, 6, 7]:
        errors.append("Invalid energy level.")

    # Validate free time.
    if not isinstance(free_time, bool):
        errors.append("Free time must be True or False.")

    # Validate weather.
    if not isinstance(weather, str) or not weather.strip():
        errors.append("Weather is required.")

    # Validate recommendations.

    if not isinstance(recommendations, str):
        errors.append("Recommendations must be a string.")

    return errors if errors else None


# GET -end point to display Home Page
@app.route("/", methods=["GET"])
def get_homepage():
    return jsonify({
        "Info": ("You can use this system by registering a new user to "
                 "add journal entries, get recommendations and to track your mood.")})

@app.route("/register", methods=["POST"])
def register():
    try:
        if not request.is_json:
            return jsonify({
                "error": "Invalid data",
                "message": "Request body is missing or not valid JSON."
            }), 400

        data = request.get_json()

        # Validate all fields before creating the user.
        errors = validate_user_fields(data)

        if errors:
            if isinstance(errors, dict):  # DB error
                return jsonify(errors), 500

            return jsonify({
                "error": "Invalid data",
                "problems": errors
            }), 400

        # Hash the password before saving it to the database.
        data["password"] = hash_password(data["password"])

        add_user = create_user(data)

        if "error" in add_user:
            return jsonify(add_user), 400

        return jsonify(add_user), 201

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "message": str(e)
        }), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        if not request.is_json:
            return jsonify({
                "status": "error",
                "message": "Request must be JSON",
                "error": "INVALID_CONTENT_TYPE"
            }), 400

        data = request.get_json()
        errors = validate_login_data(data)

        if errors:
            if isinstance(errors, dict):  # Database error
                return jsonify(errors), 500

            return jsonify({
                "error": "Invalid credentials",
                "problems": errors
            }), 401

        # Get user ID from email so the console can use it for journal actions.
        user_id = get_logged_in_user_id(data["email"])

        if not user_id:
            return jsonify({
                "error": "User not found"
            }), 404

        return jsonify({
            "message": "YOU HAVE SUCCESSFULLY LOGGED IN",
            "user_id": user_id
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/login/mood_summary", methods=["GET"])
def mood_summary():
    try:
        user_id = request.args.get("user_id")

        try:
            user_id = int(user_id)

        except (ValueError, TypeError):
            return jsonify({
                "error": "User ID must be a valid integer."
            }), 400

        if user_id <= 0:
            return jsonify({
                "error": "User ID must be greater than 0."
            }), 400

        summary = get_user_mood_summary(user_id)

        if summary is None:
            return jsonify({
                "error": "Mood data is empty."
            }), 404

        common_mood = get_common_mood_category(user_id)

        if common_mood is None:
            return jsonify({
                "error": "Mood data is empty."
            }), 404

        response = {
            "summary": summary,
            "most_common_mood": common_mood
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500



@app.route("/login/search_entries", methods=["GET"])
def search_entries():

    try:
        user_id = request.args.get("user_id")
        mood = request.args.get("mood")
        keyword = request.args.get("keyword")
        sort = request.args.get("sort", "date_desc")
        limit = request.args.get("limit", 20, type=int)

        if not user_id:
            return jsonify({"error": "user_id is required"}), 400
        try:
            user_id = int(user_id)

        except (ValueError, TypeError):
            return jsonify({
            "error": "User ID must be a valid integer."
            }), 400

        if user_id <= 0:
            return jsonify({
            "error": "User ID must be greater than 0."
            }), 400

        found_rows = get_searched_entries(user_id, mood, keyword, sort, limit)

        if found_rows is None:
            return jsonify({
                "error": "No Entries Found."
            }), 404

        response = {
            "entries": found_rows
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({
            "error": f"Server error: {str(e)}"
        }), 500

# API endpoint to retrieve all journal entries for a specific user
# Returns the user's journal entries along with a total count
@app.route('/login/journal_entries', methods=['GET'])
def view_journal_entry():

    # Get the user ID from the URL query parameters
    # Example: /login/journal_entries?user_id=1
    user_id = request.args.get("user_id")

    # Retrieve all journal entries for the specified user
    # If no entries are found, use an empty list to avoid errors when using len()
    entries = get_user_journal_entries(user_id) or []

    # Return the journal entries as a JSON response
    return jsonify({
        "user_id": user_id,
        "total_entries": len(entries),
        "entries": entries
    })

# API endpoint to update an existing journal entry
# Uses the entry_id from the URL to identify which entry to edit
@app.route('/login/journal_entries/<int:entry_id>', methods=['PUT'])
def edit_journal_entry(entry_id):
    """Update an existing journal entry"""

    try:
        # Ensure the request body is JSON
        if not request.is_json:
            return jsonify({
                "status": "error",
                "message": "Request must be JSON",
                "error": "INVALID_CONTENT_TYPE"
            }), 400

        # Retrieve the updated journal entry data from the request
        data = request.get_json()

        # Validate title and content are provided
        title = data.get("title")
        content = data.get("content")

        if not title or not title.strip():
            return jsonify({
                "status": "error",
                "message": "Title cannot be empty"
            }), 400

        if not content or not content.strip():
            return jsonify({
                "status": "error",
                "message": "Content cannot be empty"
            }), 400

        # Call the database function to update the journal entry
        updated_entry = update_journal_entry(entry_id, data)

        # If the journal entry does not exist, return a 404 response
        if "error" in updated_entry:
            return jsonify(updated_entry), 404

        # Return a success response
        return jsonify(updated_entry), 200

    except Exception as e:
        # Handle unexpected server errors
        return jsonify({"error": str(e)}), 500

# Delete a journal entry using its unique entry ID
@app.route('/login/journal_entries/<int:entry_id>', methods=['DELETE'])
def delete_journal(entry_id):

    try:
        # Validate that the entry ID is greater than 0
        if entry_id <= 0:
            return jsonify({
                "error": "Entry ID must be greater than 0"
            }), 400

        # Call the database function in db_utils.py
        result = delete_journal_entry(entry_id)

        # If the journal entry does not exist,
        # return a 404 (Not Found) response
        if "error" in result:
            return jsonify(result), 404

        # Return a success message if the entry was deleted
        return jsonify(result), 200

    except Exception as e:
        # Return an error message if something unexpected happens
        return jsonify({"error": str(e)}), 500

@app.route('/login/journal_entries', methods=['POST'])
def add_journal_entry():
    """Create a new journal entry"""

    try:
        if not request.is_json:
            return jsonify({
                "status": "error",
                "message": "Request must be JSON",
                "error": "INVALID_CONTENT_TYPE"
            }), 400

        data = request.get_json()
        errors = validate_add_journal_entry(data)

        if errors is None:
            add_row = create_journal_entry(data)
            return jsonify(add_row), 201
        else:
            return jsonify({"errors": errors}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# run flask app
if __name__ == "__main__":
    app.run(debug=False)