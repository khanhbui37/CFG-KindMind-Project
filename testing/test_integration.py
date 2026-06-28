"""
Integration tests for the Flask authentication and journal routes.

This file tests the application's integration by sending requests through
Flask's test client and checking the returned responses.

Current coverage:
- Phase 1: Authentication
- Phase 2: Journal Entries
"""

import pytest
import uuid
from app import app


# =====================================================
# Phase 1 - Authentication Integration Tests
# =====================================================


# Create a Flask test client
@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# Test successful user registration
def test_register_user(client):

    # Create a unique email
    email = f"test_{uuid.uuid4()}@example.com"

    # Send registration request
    response = client.post("/register", json={
        "name": "Integration Test User",
        "email": email,
        "password": "Password1!"
    })

    # Check registration succeeded
    assert response.status_code == 201

    data = response.get_json()

    # Check success message
    assert data["message"] == "User Successfully Added"


# Test duplicate email registration
def test_register_duplicate_email(client):

    # Create a unique email
    email = f"duplicate_{uuid.uuid4()}@example.com"

    # Register the user
    client.post("/register", json={
        "name": "Integration Test User",
        "email": email,
        "password": "Password1!"
    })

    # Try registering the same email again
    response = client.post("/register", json={
        "name": "Integration Test User",
        "email": email,
        "password": "Password1!"
    })

    # Check duplicate registration is rejected
    assert response.status_code == 400

    data = response.get_json()

    # Check error message
    assert data["error"] == "Invalid data"
    assert "Email already exists. Please Login with your email." in data["problems"]


# Test successful login
def test_login_user(client):

    # Create login details
    email = f"login_{uuid.uuid4()}@example.com"
    password = "Password1!"

    # Register the user
    client.post("/register", json={
        "name": "Login Test User",
        "email": email,
        "password": password
    })

    # Log in with the same details
    response = client.post("/login", json={
        "email": email,
        "password": password
    })

    # Check login succeeded
    assert response.status_code == 200

    data = response.get_json()

    # Check response data
    assert data["message"] == "YOU HAVE SUCCESSFULLY LOGGED IN"
    assert "user_id" in data


# Test login with an incorrect password
def test_login_invalid_password(client):

    # Create login details
    email = f"login_{uuid.uuid4()}@example.com"
    password = "Password1!"

    # Register the user
    client.post("/register", json={
        "name": "Login Test User",
        "email": email,
        "password": password
    })

    # Try logging in with the wrong password
    response = client.post("/login", json={
        "email": email,
        "password": "WrongPassword1!"
    })

    # Check login is rejected
    assert response.status_code == 401

    data = response.get_json()

    # Check error message
    assert data["error"] == "Invalid credentials"
    assert "Email and password do not match." in data["problems"]


# Test registration with invalid email format
def test_register_invalid_email(client):

    response = client.post("/register", json={
        "name": "Invalid Email User",
        "email": "notanemail",
        "password": "Password1!"
    })

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid data"
    assert "Invalid email format." in data["problems"]


# Test registration with a weak password
def test_register_weak_password(client):

    response = client.post("/register", json={
        "name": "Weak Password User",
        "email": "weak@example.com",
        "password": "hello"
    })

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid data"
    assert "Password must be at least 7 characters." in data["problems"]


# Test registration with an empty name
def test_register_empty_name(client):

    response = client.post("/register", json={
        "name": "",
        "email": "empty@example.com",
        "password": "Password1!"
    })

    assert response.status_code == 400

    data = response.get_json()

    assert data["error"] == "Invalid data"
    assert "Name cannot be empty." in data["problems"]

# =====================================================
# Phase 2 - Journal Entry Integration Tests
# =====================================================

# Test adding a journal entry
def test_add_journal_entry(client):
    # Create user details
    email = f"journal_{uuid.uuid4()}@example.com"
    password = "Password1!"

    # Register the user
    client.post("/register", json={
        "name": "Journal Test User",
        "email": email,
        "password": password
    })

    # Log in to get the user_id
    login_response = client.post("/login", json={
        "email": email,
        "password": password
    })

    login_data = login_response.get_json()
    user_id = login_data["user_id"]

    # Add a journal entry
    response = client.post("/login/journal_entries", json={
        "user_id": user_id,
        "title": "Integration Test Entry",
        "content": "This is a test journal entry.",
        "mood_category": 3,
        "mood_score": 6,
        "energy_level": 4,
        "free_time": True,
        "weather": "Cloudy",
        "recommendations": "Take a short walk."
    })

    # Check journal entry was created
    assert response.status_code == 201


# Test adding a journal entry with missing title
def test_add_journal_entry_missing_title(client):

    email = f"journal_missing_{uuid.uuid4()}@example.com"
    password = "Password1!"

    client.post("/register", json={
        "name": "Journal Test User",
        "email": email,
        "password": password
    })

    login_response = client.post("/login", json={
        "email": email,
        "password": password
    })

    login_data = login_response.get_json()
    user_id = login_data["user_id"]

    response = client.post("/login/journal_entries", json={
        "user_id": user_id,
        "title": "",
        "content": "This entry is missing a title.",
        "mood_category": 3,
        "mood_score": 6,
        "energy_level": 4,
        "free_time": True,
        "weather": "Cloudy",
        "recommendations": "Take a short walk."
    })

    assert response.status_code == 400

    data = response.get_json()
    assert "Title is required." in data["errors"]


# Test viewing journal entries
def test_view_journal_entries(client):

    email = f"journal_view_{uuid.uuid4()}@example.com"
    password = "Password1!"

    client.post("/register", json={
        "name": "Journal Test User",
        "email": email,
        "password": password
    })

    login_response = client.post("/login", json={
        "email": email,
        "password": password
    })

    user_id = login_response.get_json()["user_id"]

    client.post("/login/journal_entries", json={
        "user_id": user_id,
        "title": "View Test Entry",
        "content": "This entry should appear when viewing journal entries.",
        "mood_category": 3,
        "mood_score": 6,
        "energy_level": 4,
        "free_time": True,
        "weather": "Cloudy",
        "recommendations": "Take a short walk."
    })

    response = client.get(f"/login/journal_entries?user_id={user_id}")

    assert response.status_code == 200

    data = response.get_json()

    assert "entries" in data
    assert len(data["entries"]) >= 1


# Test editing a journal entry
def test_edit_journal_entry(client):

    email = f"journal_edit_{uuid.uuid4()}@example.com"
    password = "Password1!"

    client.post("/register", json={
        "name": "Journal Test User",
        "email": email,
        "password": password
    })

    login_response = client.post("/login", json={
        "email": email,
        "password": password
    })

    user_id = login_response.get_json()["user_id"]

    # Add a journal entry
    client.post("/login/journal_entries", json={
        "user_id": user_id,
        "title": "Original Title",
        "content": "Original content.",
        "mood_category": 3,
        "mood_score": 6,
        "energy_level": 4,
        "free_time": True,
        "weather": "Cloudy",
        "recommendations": "Take a short walk."
    })

    # View entries to get the entry_id
    view_response = client.get(f"/login/journal_entries?user_id={user_id}")
    view_data = view_response.get_json()

    entry_id = view_data["entries"][0]["entry_id"]

    response = client.put(f"/login/journal_entries/{entry_id}", json={
        "title": "Updated Title",
        "content": "Updated content."
    })

    assert response.status_code == 200

    data = response.get_json()
    assert data is not None


# Test deleting a journal entry
def test_delete_journal_entry(client):

    email = f"journal_delete_{uuid.uuid4()}@example.com"
    password = "Password1!"

    # Register the user
    client.post("/register", json={
        "name": "Journal Test User",
        "email": email,
        "password": password
    })

    # Log in to get user_id
    login_response = client.post("/login", json={
        "email": email,
        "password": password
    })

    user_id = login_response.get_json()["user_id"]

    # Add a journal entry
    client.post("/login/journal_entries", json={
        "user_id": user_id,
        "title": "Delete Test Entry",
        "content": "This entry will be deleted.",
        "mood_category": 3,
        "mood_score": 6,
        "energy_level": 4,
        "free_time": True,
        "weather": "Cloudy",
        "recommendations": "Take a short walk."
    })

    # View entries to get the entry_id
    view_response = client.get(f"/login/journal_entries?user_id={user_id}")
    view_data = view_response.get_json()

    entry_id = view_data["entries"][0]["entry_id"]

    # Delete the journal entry
    response = client.delete(
        f"/login/journal_entries/{entry_id}",
        json={}
    )

    assert response.status_code == 200

    data = response.get_json()
    assert data["message"] == "Journal Entry Successfully Deleted"


# Test searching journal entries
def test_search_journal_entries(client):

    email = f"journal_search_{uuid.uuid4()}@example.com"
    password = "Password1!"

    client.post("/register", json={
        "name": "Journal Test User",
        "email": email,
        "password": password
    })

    login_response = client.post("/login", json={
        "email": email,
        "password": password
    })

    user_id = login_response.get_json()["user_id"]

    client.post("/login/journal_entries", json={
        "user_id": user_id,
        "title": "Search Test Entry",
        "content": "This entry contains the keyword sunshine.",
        "mood_category": 3,
        "mood_score": 6,
        "energy_level": 4,
        "free_time": True,
        "weather": "Sunny",
        "recommendations": "Go outside."
    })

    response = client.get(
        f"/login/search_entries?user_id={user_id}&keyword=sunshine"
    )

    assert response.status_code == 200

    data = response.get_json()
    assert "entries" in data


# Test viewing mood summary
def test_view_mood_summary(client):

    email = f"mood_summary_{uuid.uuid4()}@example.com"
    password = "Password1!"

    client.post("/register", json={
        "name": "Mood Summary User",
        "email": email,
        "password": password
    })

    login_response = client.post("/login", json={
        "email": email,
        "password": password
    })

    user_id = login_response.get_json()["user_id"]

    client.post("/login/journal_entries", json={
        "user_id": user_id,
        "title": "Mood Summary Entry",
        "content": "Testing mood summary.",
        "mood_category": 3,
        "mood_score": 6,
        "energy_level": 4,
        "free_time": True,
        "weather": "Sunny",
        "recommendations": "Go outside."
    })

    response = client.get(f"/login/mood_summary?user_id={user_id}")

    assert response.status_code == 200

    data = response.get_json()
    assert "summary" in data
    assert "most_common_mood" in data