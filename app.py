from flask import Flask, jsonify, request
from db_utils import get_connection, get_user_mood_summary, get_common_mood_category, create_user, get_user_journal_entries
import re
import mysql.connector
from datetime import datetime

app = Flask(__name__)

#Helper function to validate user info.
def validate_user_fields (data):

    errors=[]

    user_name = data.get('name')
    user_email = data.get('email')
    user_password = data.get('password')


    if not user_name.strip():
        errors.append("Name cannot be empty.")

    if len(user_name.strip()) < 2:
        errors.append("Name must be at least 2 characters.")

    if not re.match(r"^[A-Za-z ]+$", user_name):
        errors.append("Name can only contain letters and spaces.")

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, user_email):
        errors.append("Invalid email format.")

    if len(user_password) < 7:
        errors.append("Password must be at least 7 characters.")

    if not re.search(r"[A-Z]", user_password):
        errors.append("Password must contain an uppercase letter.")

    if not re.search(r"[a-z]", user_password):
        errors.append("Password must contain a lowercase letter.")

    if not re.search(r"\d", user_password):
        errors.append("Password must contain a number.")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", user_password):
        errors.append("Password must contain a special character.")


    db = None
    cursor = None

    try:
        db = get_connection()  # connect to database
        cursor = db.cursor()

        cursor.execute("""USE kindMind""")
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

    user_password = data.get('password')
    user_email = data.get('email')

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    if not re.match(pattern, user_email):
        errors.append("Invalid email format.")

    if len(user_password) < 7:
        errors.append("Password must be at least 7 characters.")

    if not re.search(r"[A-Z]", user_password):
        errors.append("Password must contain an uppercase letter.")

    if not re.search(r"[a-z]", user_password):
        errors.append("Password must contain a lowercase letter.")

    if not re.search(r"\d", user_password):
        errors.append("Password must contain a number.")

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", user_password):
        errors.append("Password must contain a special character.")


    db = None
    cursor = None

    try:
        db = get_connection()  # connect to database
        cursor = db.cursor()

        cursor.execute("""USE kindMind""")

        query = """
        SELECT * 
        FROM users 
        WHERE email = %s AND hashed_password = %s
        """

        cursor.execute(query, (user_email, user_password))
        result = cursor.fetchone()

        if not result:
            errors.append("Email and Password doesn't match")


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
        # Validates all the fields required on creation
        errors = validate_user_fields(data)

        if errors is None:
            add_user = create_user(data)  # Add new user to users table in db_utils file

            if "error" in add_user:
                return jsonify(add_user), 400

            return jsonify(add_user), 201

        else:
            return jsonify({"error": "Invalid data", "problems": errors}), 400

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


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

        if errors is None:
            return jsonify({"message":"YOU HAVE SUCCESSFULLY LOGGED IN"}), 200

        else:
            return jsonify({"errors": errors}), 400

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
    pass


# run flask app
if __name__ == "__main__":
    app.run(debug=False)