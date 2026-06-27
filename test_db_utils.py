#===================================================================
# UNIT TESTS FOR KINDMIND DB UTILS
#===================================================================
# - mocks the database connection and cursor
# - checks database/table creation runs expected SQL
# - checks user and journal insert functions commit changes
# - checks journal view/edit/delete helpers return expected results
# - checks login user ID lookup returns the correct user_id
# - checks search helper builds keyword, mood and sort filters
# - checks common mood helper returns the most frequent mood category
# - confirms connection failures return safely instead of crashing
#===================================================================

import sys
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import mysql.connector
import pytest


# Lets db_utils import safely even if config.py is not committed.
# The real database connection is mocked in these tests.
sys.modules.setdefault(
    "config",
    SimpleNamespace(db_config={
        "host": "localhost",
        "user": "test_user",
        "password": "test_password"
    })
)

import db_utils


def make_mock_connection():
    """Create a fake database connection and cursor."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn, mock_cursor


class TestGetConnection:
    """Tests for opening a database connection."""

    def test_get_connection_success(self):
        mock_conn = MagicMock()

        with patch("db_utils.mysql.connector.connect", return_value=mock_conn) as mock_connect:
            result = db_utils.get_connection()

        assert result == mock_conn
        mock_connect.assert_called_once_with(**db_utils.db_config)

    def test_get_connection_failure_returns_none(self):
        # If MySQL connection fails, the function should return None instead of crashing.
        with patch("db_utils.mysql.connector.connect") as mock_connect:
            mock_connect.side_effect = mysql.connector.Error("Connection refused")

            result = db_utils.get_connection()

        assert result is None


class TestCreateDatabase:
    """Tests for database and table creation."""

    def test_create_database_creates_tables_and_commits(self):
        mock_conn, mock_cursor = make_mock_connection()

        with patch("db_utils.get_connection", return_value=mock_conn):
            db_utils.create_database()

        # Check the SQL statements that were sent to the cursor.
        executed = [str(call.args[0]) for call in mock_cursor.execute.call_args_list]

        assert any("CREATE DATABASE IF NOT EXISTS KindMind" in statement for statement in executed)
        assert any("users" in statement.lower() for statement in executed)
        assert any("journal_entries" in statement.lower() for statement in executed)

        # Default mood/energy values should be inserted.
        assert mock_cursor.executemany.call_count == 3
        mock_conn.commit.assert_called_once()

    def test_create_database_closes_connection(self):
        mock_conn, mock_cursor = make_mock_connection()

        with patch("db_utils.get_connection", return_value=mock_conn):
            db_utils.create_database()

        # Connections should be closed after use.
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    def test_create_database_handles_mysql_error(self):
        mock_conn, mock_cursor = make_mock_connection()
        mock_cursor.execute.side_effect = mysql.connector.Error("SQL error")

        with patch("db_utils.get_connection", return_value=mock_conn):
            try:
                db_utils.create_database()
            except Exception:
                pytest.fail("create_database() should handle MySQL errors without crashing")


class TestCreateUser:
    """Tests for inserting users."""

    def test_create_user_success(self):
        mock_conn, mock_cursor = make_mock_connection()

        data = {
            "name": "Aamna",
            "email": "aamna@example.com",
            "password": "hashed-password"
        }

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.create_user(data)

        assert result == {"message": "User Successfully Added"}
        mock_conn.commit.assert_called_once()

        # The last execute call should be the INSERT statement.
        insert_call = mock_cursor.execute.call_args_list[-1]
        assert "INSERT INTO users" in insert_call.args[0]
        assert insert_call.args[1] == ("Aamna", "aamna@example.com", "hashed-password")

    def test_create_user_integrity_error(self):
        mock_conn, mock_cursor = make_mock_connection()

        # First execute is USE KindMind, second execute is the INSERT.
        mock_cursor.execute.side_effect = [
            None,
            mysql.connector.IntegrityError("Duplicate email")
        ]

        data = {
            "name": "Aamna",
            "email": "aamna@example.com",
            "password": "hashed-password"
        }

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.create_user(data)

        assert "error" in result
        assert "Integrity error" in result["error"]


class TestJournalEntryDatabaseFunctions:
    """Tests for creating, viewing, editing and deleting journal entries."""

    def test_create_journal_entry_success(self):
        mock_conn, mock_cursor = make_mock_connection()

        data = {
            "user_id": 1,
            "title": "Test title",
            "content": "Test content",
            "mood_category": 3,
            "mood_score": 5,
            "energy_level": 4,
            "free_time": True,
            "weather": "Clouds",
            "recommendations": "Take a short walk."
        }

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.create_journal_entry(data)

        assert result == {"message": "Journal Entry Successfully Added"}
        mock_conn.commit.assert_called_once()

        insert_call = mock_cursor.execute.call_args_list[-1]
        assert "INSERT INTO journal_entries" in insert_call.args[0]
        assert insert_call.args[1] == (
            1,
            "Test title",
            "Test content",
            3,
            5,
            4,
            True,
            "Clouds",
            "Take a short walk."
        )

    def test_get_user_journal_entries_returns_entries(self):
        mock_conn, mock_cursor = make_mock_connection()
        mock_entries = [{"entry_id": 1, "title": "Entry 1"}]
        mock_cursor.fetchall.return_value = mock_entries

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.get_user_journal_entries(1)

        assert result == mock_entries

        # Query should look up entries for the supplied user_id.
        query_call = mock_cursor.execute.call_args_list[-1]
        assert "FROM journal_entries" in query_call.args[0]
        assert query_call.args[1] == (1,)

    def test_update_journal_entry_success(self):
        mock_conn, mock_cursor = make_mock_connection()
        mock_cursor.rowcount = 1

        data = {
            "title": "Updated title",
            "content": "Updated content"
        }

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.update_journal_entry(10, data)

        assert result == {"message": "Journal Entry Successfully Updated"}
        mock_conn.commit.assert_called_once()

    def test_update_journal_entry_not_found(self):
        mock_conn, mock_cursor = make_mock_connection()
        mock_cursor.rowcount = 0

        data = {
            "title": "Updated title",
            "content": "Updated content"
        }

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.update_journal_entry(999, data)

        assert result == {"error": "Journal entry not found"}

    def test_delete_journal_entry_success(self):
        mock_conn, mock_cursor = make_mock_connection()
        mock_cursor.rowcount = 1

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.delete_journal_entry(10)

        assert result == {"message": "Journal Entry Successfully Deleted"}
        mock_conn.commit.assert_called_once()

    def test_delete_journal_entry_not_found(self):
        mock_conn, mock_cursor = make_mock_connection()
        mock_cursor.rowcount = 0

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.delete_journal_entry(999)

        assert result == {"error": "Journal entry not found"}


class TestUserLookupAndSearch:
    """Tests for login lookup, search and summary helpers."""

    def test_get_logged_in_user_id_found(self):
        mock_conn, mock_cursor = make_mock_connection()
        mock_cursor.fetchone.return_value = {"user_id": 7}

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.get_logged_in_user_id("aamna@example.com")

        assert result == 7
        mock_conn.cursor.assert_called_once_with(dictionary=True)

    def test_get_logged_in_user_id_not_found(self):
        mock_conn, mock_cursor = make_mock_connection()
        mock_cursor.fetchone.return_value = None

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.get_logged_in_user_id("missing@example.com")

        assert result is None

    def test_get_searched_entries_filters_keyword_mood_and_sort(self):
        mock_conn, mock_cursor = make_mock_connection()
        mock_rows = [{"entry_id": 1, "title": "Walk"}]
        mock_cursor.fetchall.return_value = mock_rows

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.get_searched_entries(
                user_id=1,
                mood=3,
                keyword="walk",
                sort="date_asc",
                limit=5
            )

        assert result == mock_rows

        query, params = mock_cursor.execute.call_args_list[-1].args

        # Check that mood filtering, keyword search and date sorting are included.
        assert "mood_category_id = %s" in query
        assert "title LIKE %s" in query
        assert "ORDER BY created_at ASC" in query
        assert params == [1, 3, "%walk%", "%walk%", 5]

    def test_get_common_mood_category_returns_name(self):
        mock_conn, mock_cursor = make_mock_connection()
        mock_cursor.fetchone.return_value = {"category_name": "Positive", "count": 3}

        with patch("db_utils.get_connection", return_value=mock_conn):
            result = db_utils.get_common_mood_category(1)

        assert result == "Positive"