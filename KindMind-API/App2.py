"""Kind Mind API entry point."""

from flask import Flask, jsonify, request

App = Flask(__name__)

# In-memory journal store for the current prototype.
journals = {}


def validate_journal_fields(data):
    errors = []
    required_fields = ["Title", "Content"]

    for field in required_fields:
        if not data.get(field):
            errors.append(f"{field} is required")

    return errors


@app.route("/KindMind/journals", methods=["POST"])
def create_journal_entry():
    """Create a new journal entry."""
    # Read the incoming JSON payload from the client request.
    data = request.get_json(silent=True) or {}

    # Validate the required fields before saving anything.
    errors = validate_journal_fields(data)
    if errors:
        return jsonify({"error": "Invalid journal data", "problems": errors}), 400

    # Generate the next journal ID and store the new entry in memory.
    entry_id = len(journals) + 1
    journals[entry_id] = {
        "id": entry_id,
        "Title": data.get("Title"),
        "Content": data.get("Content"),
        "Mood": data.get("Mood", "Unknown"),
        "Energy Level": data.get("Energy Level", "Not set"),
        "Free Time": data.get("Free Time", ""),
        "Created At": data.get("Created At", "Now"),
    }

    return jsonify({"message": "Journal entry created successfully.", "entry": journals[entry_id]}), 201


@app.route("/KindMind/journals/<int:entry_id>", methods=["PUT"])
def update_journal_entry(entry_id):
    """Update an existing journal entry, or create one if it does not yet exist."""
    # Read the incoming update payload from the request body.
    data = request.get_json(silent=True) or {}

    # If this journal ID does not exist yet, create it using the same validation rules.
    if entry_id not in journals:
        errors = validate_journal_fields(data)
        if errors:
            return jsonify({"error": "Invalid journal data", "problems": errors}), 400

        journals[entry_id] = {
            "id": entry_id,
            "Title": data.get("Title"),
            "Content": data.get("Content"),
            "Mood": data.get("Mood", "Unknown"),
            "Energy Level": data.get("Energy Level", "Not set"),
            "Free Time": data.get("Free Time", ""),
            "Created At": data.get("Created At", "Now"),
        }
        return jsonify({"message": "Journal entry created successfully.", "entry": journals[entry_id]}), 201

    # Merge the submitted values into the existing entry without losing current data.
    journals[entry_id].update({
        "Title": data.get("Title", journals[entry_id]["Title"]),
        "Content": data.get("Content", journals[entry_id]["Content"]),
        "Mood": data.get("Mood", journals[entry_id]["Mood"]),
        "Energy Level": data.get("Energy Level", journals[entry_id]["Energy Level"]),
        "Free Time": data.get("Free Time", journals[entry_id]["Free Time"]),
        "Created At": data.get("Created At", journals[entry_id]["Created At"]),
    })

    return jsonify({"message": "Journal entry updated successfully.", "entry": journals[entry_id]}), 200


@app.route("/KindMind/journals", methods=["GET"])
def list_journals():
    return jsonify({"journals": list(journals.values())}), 200


if __name__ == "__main__":
    App.run(debug=True)




                
