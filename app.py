from flask import Flask, jsonify, request
from db_utils import get_connection, get_user_mood_summary, get_common_mood_category, create_user, create_journal_entry, get_searched_entries
from werkzeug.security import hashed_password 
import hashlib
import re
import mysql.connector

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

# Helper Function to validate hashing 
#protecting users content and personal info 
def hash_entry(user_id, title, content):
    data = f"{user_id}:{title}:{content}"
    return hashlib.sha256(data.encode()).hexdigest()

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

    if len(title.strip()) > 100:
        errors.append("Title cannot exceed 100 characters.")

    # Validate content.
    if not isinstance(content, str) or not content.strip():
        errors.append("Content is required.")

    if len(content) > 5000:
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
@app.route("/homepage", methods=["GET"])
def get_homepage():

    return "Welcome to KindMind !"
    jsonify({
        "Info": ("You can use this system by registering a new user to "
                 "add journal entries, get recommendations and to track your mood.")})

@app.route("verify/register", methods=["POST"])
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
            data['password'] = user.hash_password(data['password']) # starts hashing inputted password 
            add_user = create_user(data)  # Add new user to users table in db_utils file

            if "error" in add_user:
                return jsonify(add_user), 400

            return jsonify(add_user), 201

        else:
            return jsonify({"error": "Invalid data", "problems": errors}), 400

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500


@app.route("/login/verify/", methods=["POST"])
def login():
    try:
        if not request.is_json:
            return jsonify({
                    "status": "error",
                    "message": "Request must be JSON",
                    "error": "INVALID_CONTENT_TYPE"
                }), 400
        
        # checks if customer data lines up with the database 
        if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    

        data = request.get_json()
        errors = validate_login_data(data)  # validate data in a helper function
        access = create_access(identity=user.id) # access to be granted 
            
        if errors is None:

            return jsonify({"message":"YOU HAVE SUCCESSFULLY LOGGED IN",
                            " access": hashed_entry, # add hashed function
                            "user_id" : user_id
            }), 200

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
entry.integrity_hash = hash_entry(user_id,entry.title,entry.content)
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

        if errors is None:
            add_row = create_journal_entry(data)   # Add journal entry to table in db_utils file
            return jsonify(add_row), 201
        else:
            return jsonify({"errors": errors}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# run flask app
if __name__ == "__main__":
    app.run(debug=False)