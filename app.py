from flask import Flask, jsonify, request
from db_utils import get_user_mood_summary, get_common_mood_category

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():
    pass

@app.route("/mood_summary", methods=["POST"])
def mood_summary():
    data = request.get_json()

    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "user_id is required"}), 400
#yet to implement validations for date
    summary = get_user_mood_summary(user_id)
    if not summary:
        return jsonify({"error": "No data found"}), 404

    common_mood = get_common_mood_category(user_id)

    response = {
        "summary": summary,
        "most_common_mood": common_mood
    }

    return jsonify(response)









# run flask app
if __name__ == "__main__":
    app.run(debug=False)