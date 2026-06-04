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
import db_utils_sql as db_utils 

App = Flask(__name__)

def validate_user_fields (data, require_all=False): #data will be from the SQL
    errors=[] # could add while loop for amount of errors in login
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

@app.route("/api/user", methods=["POST"])
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
        
         #checks if data already exits in the system
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


if __name__ == "__main__":
    App.run(debug=True)




                
