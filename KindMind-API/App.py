"""
Kind Mind app.py
using flask rest API postman

Users >

POST api/ users  -( adds data for customers register)
PUT api/users/<id>  -(updates user data to login, creates and edits journals)
GET api/users -(collects weather data to create a quote)
DELETE api/user/<id> -(delete journal entries)
"""

from flask import Flask, request,jsonify
import db_utils 

App = Flask(__name__)

def validate_user_fields (data, require_all=False): #data will be from the SQL
    errors=[] # could add while loop for amount of errors in login
    int limit = 3 # max attempts for login
    int mistakeCount = 0 # counting up till 3 limits

    while mistakeCount < limit:
    required_fields = ["username", "password"]

    for field in required_fields:
        if require_all or field in data:
            if field not in data:
                errors.append(f"{field} is required!!")
            else:
                value = data [field]
                # inputs of the SQL later

return errors    



# user end point 
# POST api/ users  -( adds data for customers register)

@app.route("/KindMind/users", methods=["POST"])
def create_customer():
    """
    Json format
    {
    "username": "Jenny Watkins",
    "password": password123
    }
    """

    try:
        data = request.get_json()
        if not data:
            return jsonify({
                "error":   "Invalid data",
                "message": "Request body is missing or not valid JSON."
            }), 400

        # Validates all the fields required on creation
        errors = validate_customer_fields(data, require_all=True)
        if errors:
            return jsonify({"error": "Invalid data", "problems": errors}), 400

        # new users inputted into database 

         new_id = db_utils.create_user(
            data["username"],
            data["password"]
         )
        
         #checks if data already exists in the system
            if db_utils.get_user_by_username(data["username"]):
                return jsonify({"error": "Username already exists"}), 400

        # Successful new user created 
         user = db_utils.get_user_by_id(new_id)
        return jsonify({
            "message":  "User registered successfully.",
            "user": user
        }), 201                   

    except Exception as e:
        return jsonify({"error": "Internal server error", "message": str(e)}), 500



# PUT api/ users /<id>  -(updates user data to login, creates and edits journals)
#Login section 

 @app.route("/KindMind/users/<login:id>", methods=["PUT"])
 def login_user(id):
    """
    Json format
    {
    "username": "Jenny Watkins",
    "password": password123
    }
    """
    # This will verfiy if the customer exists in the sysstem

    try:
        user = db_utils.get_user_by_id(user_id)
        if not user:
            return jsonify({
                "error": "User not found",
                "user_id": user_id,
                "message": f"This {user_id} does not exist."
            }), 404

# Create  journal section      
@app.route("/KindMind/users/<create_journalentries:id>", methods=["PUT"])
def create_journal(entry_id):

    data = request.get_json()
    if not data:
        return jsonify({
            "error":   "Invalid data",
            "message": "Request body is missing or not valid JSON."
        }), 400
    """
    Json format
    {
    "Title": "My Day",
    "Content": "Today was a good day!"
    "Mood": "Happy"
    "energy level": "High"
    "Free Time" : "Workout, reading, knitting"
    "Created At": "21:53 06/06/2026"
    }
    """
    
    entry = journalentries.query.get(entry_id)
   # Creates journal section
    if entry:
        entry.Title = data.get("Title", JournalEntries.Title)
        entry.Content = data.get("Content", JournalEntries.Content)
        entry.Mood = data.get("Mood", JournalEntries.Mood)
        entry.Energy_Level = data.get("Energy Level",JournalEntries.Energy_Level)
        entry.Free_Time = data.get("Free Time",JournalEntries.Free_Time)
        entry.Created_At = data.get("Created At", JournalEntries.Created_At)

        else:
            if not data.get("Title") or not data.get("Content"):
                return jsonify({
                    "error": "Title and Content are required fields for creating a journal entry."
                }), 400

        db.session.commit()

        return jsonify({
            "message": "Journal entry updated successfully.",
            "entry": {
                "id": entry.id,
                "Title": entry.Title,
                "Content": entry.Content,
                "Mood": entry.Mood,
                "Energy Level": entry.Energy_Level,
                "Free Time": entry.Free_Time,
                "Created At": entry.Created_At
            }
        }), 200






if __name__ == "__main__":
    App.run(debug=True)




                
