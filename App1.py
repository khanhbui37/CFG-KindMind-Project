"""
Kind Mind app.py
using flask rest API postman

Users >

POST api/ users  -( adds data for customers register, login and create entries)
PUT api/users/<id>  -(updates user data and edits journals)
GET api/users -(collects weather data to create recommedation quote and get specific entries, as well as filtering searches)
DELETE api/user/<id> -(delete journal entries)
"""

from flask import Flask, request,jsonify
import db_utils 
import hashlib

App = Flask(__name__)

# authentication section 

@app.route("/KindMind/authenticate/register", methods=["POST"])
def register_user():
     """Register a new user"""
    data = request.get_json()
    
    # Validate input
    if not data or not data.get('username') or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Missing required fields: username, email, password"}), 400
    
    # Check if user exists
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already registered"}), 409
    
    # Create new user
    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        "message": "User registered successfully",
        "user_id": user.id,
        "username": user.username
    }), 201
 
 # Login section
@app.route('/KindMind/auth/login', methods=['POST'])
def login():

    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Missing username or password"}), 400
    
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Create access (through Flask)
    access = create_access(identity=user.id)
    hashed_access = hashlib.sha256(access.encode()).hexdigest()  # Hash the access token for security
    
    return jsonify({
        "message": "Login successful",
        "access": hashed_access,
        "user_id": user.id
    }), 200

# CRUD for journal entries

@app.route('/KindMind/entries', methods=['POST'])
def create_entry():
    """Create a new journal entry"""
    user_id = get_user_id()
    data = request.get_json()
    
    # Validate required fields
    required = ['title', 'content', 'mood', 'energy_level', 'free_time']
    if not all(field in data for field in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400
    
    #Validate MoodCategory valuees
     valid_moodscat = ['Negative', 'Neutral', 'Positive', 'Ambiguous']
    if data['mood'] not in valid_moodscat:
        return jsonify({"error": f"Invalid mood category. Must be one of: {valid_moodscat}"}), 400
    
    # Validate moodscore value
    # added moods that the user can input 
    valid_moods = ['Terrible', 'Bad', 'anxious', 'calm', 'ok','excited','happy']
    if data['mood'] not in valid_moods:
        return jsonify({"error": f"Invalid mood. Must be one of: {valid_moods}"}), 400
    
    # Validate energy level (1-7)
    # Not sure of measurement.
    energy_level = [1 = 'drained', 2 = 'sluggish', 3 = 'mellow', 4 = 'steady', 5 = 'vibrant', 6 = 'driven', 7 = 'radiant']
    if not (1 <= data['energy_level'] <= 7):
        return jsonify({"error": "Energy level must be between 1 and 7"}), 400
    
    # Fetch weather data if location provided
    weather_condition = None
    weather_temp = None
    if 'location' in data:
        weather = get_weather(data['location'])
        if weather:
            weather_condition = weather['condition']
            weather_temp = weather['temp']
    
    # Create entry
    entry = JournalEntry(
        user_id=user_id,
        title=data['title'],
        content=data['content'],
        mood=data['mood'],
        energy_level=data['energy_level'],
        free_time=data['free_time'],
        weather_condition=weather_condition,
        weather_temp=weather_temp
    )
    
    db.session.add(entry)
    db.session.commit()
    
    return jsonify({
        "message": "Entry created",
        "entry": entry.to_dict()
    }), 201

# Update entries in the journal 
@app.route('/KindMind/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """Update a single journal entry"""
    user_id = get_user_id()
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first()
    
    if not entry:
        return jsonify({"error": "Entry not found"}), 404

    data = request.get_json()
    
    # Update entry fields
    entry.title = data.get('title', entry.title)
    entry.content = data.get('content', entry.content)
    entry.mood = data.get('mood', entry.mood)
    entry.energy_level = data.get('energy_level', entry.energy_level)
    entry.free_time = data.get('free_time', entry.free_time)

    db.session.commit()

    return jsonify({
        "message": "Entry updated",
        "entry": entry.to_dict()
    }), 200
        return jsonify({"error": "Entry not found"}), 404
    
    return jsonify(entry.to_dict()), 200
 
 # entries list section
@app.route('/KindMind/entries', methods=['GET'])
def list_entries():
    # added these parameters to filter easier 
    """
    List all entries with filtering, searching and sorting
    Query params:
    - mood: filter by mood
    - keyword: search in title/content
    - sort: 'date_asc' or 'date_desc'
    - limit: number of entries (default 20)
    """
    user_id = get_user_id()
    
    # Base query
    query = JournalEntry.query.filter_by(user_id=user_id)
    
    # Filter by mood
    mood = request.args.get('mood')
    if mood:
        query = query.filter_by(mood=mood)
    
    # Search by keyword
    keyword = request.args.get('keyword')
    if keyword:
        query = query.filter(
            or_(
                JournalEntry.title.ilike(f'%{keyword}%'),
                JournalEntry.content.ilike(f'%{keyword}%')
            )
        )
    
    # Sort
    sort = request.args.get('sort', 'date_desc')
    if sort == 'date_asc':
        query = query.order_by(JournalEntry.created_at.asc())
    else:
        query = query.order_by(JournalEntry.created_at.desc())
    
    # Pagination 
    """
    Creates a limit number of entries to return in this case(default 20)
    """
    limit = request.args.get('limit', 20, type=int)
    entries = query.limit(limit).all()
    
    return jsonify({
        "count": len(entries),
        "entries": [entry.to_dict() for entry in entries]
    }), 200
 

# Update journal entries section
 @app.route('/KindMind/entries/<int:entry_id>', methods=['PUT'])
def update_entry(entry_id):
    """Update an existing journal entry"""
    user_id = update_entry()
    entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first()
    
    if not entry:
        return jsonify({"error": "Entry not found"}), 404
    
    data = request.get_json()
    
    # Update only provided fields
    entry.title = data.get('title', entry.title)
    entry.content = data.get('content', entry.content)
    
    if 'mood' in data:
        valid_moods = ['happy', 'sad', 'anxious', 'calm', 'excited', 'neutral', 'frustrated']
        if data['mood'] not in valid_moods:
            return jsonify({"error": f"Invalid mood"}), 400
        entry.mood = data['mood']
    
    if 'energy_level' in data:
        if not (1 <= data['energy_level'] <= 7):
            return jsonify({"error": "Energy level must be 1-7"}), 400
        entry.energy_level = data['energy_level']
    
    entry.free_time = data.get('free_time', entry.free_time)
    
    db.session.commit()
    
    return jsonify({
        "message": "Entry updated",
        "entry": entry.to_dict()
    }), 200

# Delete journal entries section
@app.route("/KindMind/entries/<int:entry_id>", methods=["DELETE"])
    # Weather connection section
    def delete_entry(entry_id):
        user_id = get_user_id()
        entry = JournalEntry.query.filter_by(id=entry_id, user_id=user_id).first()

        if not entry:
            return jsonify({"error": "Entry not found"}), 404

        db.session.delete(entry)
        db.session.commit()

        return jsonify({"message": " JournalEntry deleted"}), 200

   
   
   
   # Weather API connection section 
   
def get_weather(location):
    # location inputted by user, to connect to weather API
try:
    # this is where the API is called (openWeathermap API)
    #input API key  in the (YOUR_API_KEY) section
    # not sure if this is right format for API call.
    response = requests.get(https://api.openweathermap.org/data/4.0/onecall/current?lat={lat}&lon={lon}&appid={API key}

    parameters = { "format": "json" }
)
 
if response.status_code != 200:
    data = response.json().get("data"):
    return None

# Get weather condition and temperature

if weather_response.status_code == 200:
    data = weather_response.json()['current']
    weather_code = data['weather_code']

# weather conditions overview

condition_map = {
   0: 'clear', 1: 'mostly_clear', 2: 'partly_cloudy', 3: 'overcast',
   45: 'foggy', 48: 'foggy', 51: 'light_drizzle', 53: 'moderate_drizzle',
   55: 'dense_drizzle', 61: 'slight_rain', 63: 'moderate_rain',
   65: 'heavy_rain', 71: 'slight_snow', 73: 'moderate_snow', 75: 'heavy_snow'
}

return {
    "condition": condition_map.get(weather_code, 'unknown'),
    "temp": data['temp']
}

except Exception as e:
    print(f"Error fetching weather data: {e}")
    
return None

# recommendations section


if __name__ == "__main__":
    App.run(debug=True)