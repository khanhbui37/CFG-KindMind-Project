from flask import Flask, jsonify, request
from db_utils import (
    get_connection,
    get_user_mood_summary,
    get_common_mood_category,
    create_user,
    create_journal_entry,
    get_searched_entries,
    get_logged_in_user_id
)
from werkzeug.security import generate_password_hash, check_password_hash
import re
import mysql.connector

app = Flask(__name__)


# Hash password before saving it to the database
def hash_password(password):
    return generate_password_hash(password)

# Check typed password against the stored password hash
def verify_password(stored_hash, password): 
    return check_password_hash(stored_hash, password)

# Helper function to validate user info.
def validate_user_fields (data):

    errors=[]

    # Get user registration fields from the request body.
    # Default to an empty string so validation does not crash if a field is missing.
    user_name = data.get("name", "")
    user_email = data.get("email", "")
    user_password = data.get("password", "")

    # Name validation
    # Check that the name is a string and is not empty/only spaces.
    if not isinstance(user_name, str) or not user_name.strip():
        errors.append("Name cannot be empty.")

    # Check that the name has at least 2 characters after removing extra spaces.
    elif len(user_name.strip()) < 2:
        errors.append("Name must be at least 2 characters.")

    # Check that the name only contains letters and spaces.
    elif not re.match(r"^[A-Za-z ]+$", user_name):
        errors.append("Name can only contain letters and spaces.")
    
    # Email validation
    # Check that email is a string and matches a basic email format.
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not isinstance(user_email, str) or not re.match(pattern, user_email):
        errors.append("Invalid email format.")

    # Password validation
    # Check that password is a string and meets the minimum length requirement.
    if not isinstance(user_password, str) or len(user_password) < 7:
        errors.append("Password must be at least 7 characters.")

    # Check that password contains at least one uppercase letter.
    elif not re.search(r"[A-Z]", user_password):
        errors.append("Password must contain an uppercase letter.")

    # Check that password contains at least one lowercase letter.
    elif not re.search(r"[a-z]", user_password):
        errors.append("Password must contain a lowercase letter.")

    # Check that password contains at least one number.
    elif not re.search(r"\d", user_password):
        errors.append("Password must contain a number.")

    # Check that password contains at least one special character.
    elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", user_password):
        errors.append("Password must contain a special character.")

   # If basic validation has already failed, return the errors before checking the database.
    if errors:
        return errors
    
   # Checks if email exists already
    db = None
    cursor = None

    try:
        db = get_connection()  # connect to database
        cursor = db.cursor()

        cursor.execute("""USE KindMind""")
        cursor.execute("SELECT * FROM users WHERE email= %s", (user_email,))
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
    # Default to empty strings so missing fields do not crash validation.
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
    # Check that email matches a basic email format.
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, user_email):
        errors.append("Invalid email format.")

    # Password validation
    # Check that password meets the minimum length requirement.
    if len(user_password) < 7:
        errors.append("Password must be at least 7 characters.")

    # Check that password contains at least one uppercase letter.
    elif not re.search(r"[A-Z]", user_password):
        errors.append("Password must contain an uppercase letter.")

    # Check that password contains at least one lowercase letter.
    elif not re.search(r"[a-z]", user_password):
        errors.append("Password must contain a lowercase letter.")

    # Check that password contains at least one number.
    elif not re.search(r"\d", user_password):
        errors.append("Password must contain a number.")

    # Check that password contains at least one special character.
    elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", user_password):
        errors.append("Password must contain a special character.")


    # verifies data in DB
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

    return "Welcome to KindMind !"
    jsonify({
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
        errors = validate_login_data(data)  # validate data in a helper function

        if errors:
            if isinstance(errors, dict):  # Database error
                return jsonify(errors), 500
            return jsonify({
                "error": "Invalid credentials",
                "problems": errors
            }), 401
           
        
        # From db_utils
        # makes the app accept either a name or email
        # gets User ID info from email
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


@app.route('/login/journal_entries', methods=['GET'])
def view_journal_entry():
    pass

@app.route('/login/journal_entries', methods=['POST'])
def add_journal_entry():
    """Create a new journal entry"""
# shows user if data has been modified 
    try:
        if not request.is_json:
            return jsonify({
                    "status": "error",
                    "message": "Request must be JSON",
                    "error": "INVALID_CONTENT_TYPE"
                }), 400

        data = request.get_json()
        errors = validate_add_journal_entry(data)
        print(errors)# validate data in a helper function

        if errors:
            return jsonify({
                "error": "Invalid journal data",
                "problems": errors
            }), 400

        if errors is None:
            add_row = create_journal_entry(data)   # Add journal entry to table in db_utils file
            return jsonify(add_row), 201
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# run flask app
if __name__ == "__main__":
    app.run(debug=False)