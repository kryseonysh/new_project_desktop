#users.py
import psycopg2
from db import connect_db

def verify_user(username, password):
    """Verify user credentials."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT password FROM users WHERE username = %s;", (username,))
            result = cursor.fetchone()
            if result and result[0] == password:
                return True
            else:
                return False
        finally:
            cursor.close()
            conn.close()
    return False

def register_user(username, email, password, role):
    """Register a new user."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s);",
                           (username, email, password, role))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка регистрации пользователя: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def getUserRole(username):
    """Get user role"""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT role FROM users WHERE username = %s;", (username,))
            result = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка прочтения роли: {e}")
        finally:
            cursor.close()
            conn.close()
    return result

def getUserEmail(username):
    """Get user email"""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT email FROM users WHERE username = %s;", (username,))
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка прочтения email: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

def get_all_users():
    """Get all users"""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users;")
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка чтения пользователей: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []