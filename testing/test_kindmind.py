import pytest
from unittest.mock import patch, MagicMock, call
import mysql.connector
 
 
# ─────────────────────────────────────────────
# db_utils tests
# ─────────────────────────────────────────────
 
class TestGetConnection:
    """Tests for get_connection()"""
 
 #Testing if it connects to MySQL
    @patch("db_utils.mysql.connector.connect")
    def test_get_connection_success(self, mock_connect):
        """Returns a connection object when credentials are valid"""
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
 
        from db_utils import get_connection
        result = get_connection()
 
        assert result == mock_conn
 
 #Check it returns None instead of crashing when MySQL is down
    @patch("db_utils.mysql.connector.connect")
    def test_get_connection_failure_returns_none(self, mock_connect):
        """Returns None when connection fails"""
        mock_connect.side_effect = mysql.connector.Error("Connection refused")
 
        from db_utils import get_connection
        result = get_connection()
 
        assert result is None
 
 
class TestCreateDatabase:
    """Tests for create_data_base()"""

 #Testing if it runs CREATE database
    @patch("db_utils.get_connection")
    def test_creates_database(self, mock_get_conn):
        """Executes CREATE DATABASE statement"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
 
        from db_utils import create_data_base
        create_data_base()

 #Grab what was executed and put in a list
        executed_statements = [str(c.args[0]) for c in mock_cursor.execute.call_args_list]
        assert any("CREATE DATABASE" in s for s in executed_statements)
 
# Test that create_data_base() executes a CREATE TABLE statement for the users table
    @patch("db_utils.get_connection")
    def test_creates_users_table(self, mock_get_conn):
        """Executes CREATE TABLE for users"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
 
        from db_utils import create_data_base
        create_data_base()
 
        executed_statements = [str(c.args[0]) for c in mock_cursor.execute.call_args_list]
        assert any("users" in s.lower() for s in executed_statements)
 
 #Test that create_data_base() executes a CREATE TABLE statement for the mood_category table
    @patch("db_utils.get_connection")
    def test_creates_mood_category_table(self, mock_get_conn):
        """Executes CREATE TABLE for mood_category"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
 
        from db_utils import create_data_base
        create_data_base()
 
        executed_statements = [str(c.args[0]) for c in mock_cursor.execute.call_args_list]
        assert any("mood_category" in s.lower() for s in executed_statements)
 
 # Test that create_data_base() commits the transaction after creating the tables 
    @patch("db_utils.get_connection")
    def test_commits_after_table_creation(self, mock_get_conn):
        """Commits the transaction after creating tables"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
 
        from db_utils import create_data_base
        create_data_base()
 
        mock_conn.commit.assert_called_once()
 
 # Test that create_data_base() closes the cursor and connection after successfully creating the tables
    @patch("db_utils.get_connection")
    def test_closes_connection_on_success(self, mock_get_conn):
        """Always closes cursor and connection after success"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
 
        from db_utils import create_data_base
        create_data_base()
 
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
 
 #Test that create_data_base() does not crash if db error occurs, it should fail gracefully
    @patch("db_utils.get_connection")
    def test_handles_db_error_gracefully(self, mock_get_conn):
        """Does not raise an exception when a DB error occurs"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = mysql.connector.Error("Syntax error")
 
        from db_utils import create_data_base
 
        # Should not raise
        try:
            create_data_base()
        except Exception:
            pytest.fail("create_data_base() raised an exception unexpectedly")
 
 #Test that create_data_base() still closes the cursor and connection even when a database error occurs
    @patch("db_utils.get_connection")
    def test_closes_connection_on_error(self, mock_get_conn):
        """Closes cursor and connection even when an error occurs"""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = mysql.connector.Error("Syntax error")
 
        from db_utils import create_data_base
        create_data_base()
 
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()
 
 
# ─────────────────────────────────────────────
# main.py menu flow tests
# ─────────────────────────────────────────────
 
class TestMainMenuFlow:
    """Tests for the console menu run() function"""
# Test that when the user enters 1 in the menu, the register function is called
    @patch("main.post_register_info") # replace the real register function with a fake one
    @patch("builtins.input", return_value="1") # pretend the user typed 1
    def test_input_1_calls_register(self, mock_input, mock_register):
        """Entering 1 calls post_register_info()"""
        from main import run #bring in the menu function
        run() #run the menu
        mock_register.assert_called_once() #check the register was called once

 # Test that when the user enters 2 in the menu, the login function is called
    @patch("main.post_login_info")
    @patch("builtins.input", return_value="2")
    def test_input_2_calls_login(self, mock_input, mock_login):
        """Entering 2 calls post_login_info()"""
        from main import run
        run()
        mock_login.assert_called_once()
 
 # Test that when the user enters 3 in the menu, the program exits
    @patch("builtins.input", return_value="3")
    def test_input_3_exits(self, mock_input):
        """Entering 3 exits the program"""
        from main import run #bring in the menu function
        with pytest.raises(SystemExit): #Check the program exists
            run()
 
# Test that if the user enters an invalid option first, the menu asks again
    @patch("main.post_register_info")
    @patch("builtins.input", side_effect=["9", "1"])
    def test_invalid_input_then_valid(self, mock_input, mock_register):
        """Invalid input is ignored; valid input on retry is handled"""
        from main import run
        run()
        mock_register.assert_called_once()