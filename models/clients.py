#clients.py
import psycopg2
from db import connect_db

def add_client(name, surname, fathersname, passport, number, email, address, status):
    """Add a new client to the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                'CALL add_new_client(%s, %s, %s, %s, %s, %s, %s, %s)',
                (name, surname, fathersname, passport, number, email, address, status)
            )
            conn.commit()
            return True 
        except Exception as e:
            print(f"Ошибка добавления клиента: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_all_clients():
    """Fetch all clients from the database."""
    conn = connect_db()
    clients = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM clients;")
            clients = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка прочтения клиентов: {e}")
        finally:
            cursor.close()
            conn.close()
    return clients

def update_client_field(client_id, field_name, new_value):
    """Update a specific field of a client in the database."""
    valid_fields = ['name', 'surename', 'fathersname', 'passport', 'number', 'email', 'address', 'status']
    
    if field_name not in valid_fields:
        raise ValueError(f"Invalid field name: {field_name}. Valid fields are: {valid_fields}")

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = f"UPDATE clients SET {field_name} = %s WHERE client_Id = %s;"
            cursor.execute(query, (new_value, client_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка изменения информации о клиенте: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def delete_client(client_id):
    """Delete a client from the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM clients WHERE client_Id = %s;", (client_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка удаления клиента: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_client_by_email(email):
    """Get a client by their email address."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM clients WHERE email = %s;", (email,))
            client_data = cursor.fetchone()
            return client_data
        except Exception as e:
            print(f"Ошибка прочтения клиента: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None

def get_full_name(client_id):
    """Get the full name of a client by their ID."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT get_full_name(%s);", (client_id,))
            full_name = cursor.fetchone()
            return full_name[0] if full_name else None
        except Exception as e:
            print(f"Ошибка получения имени клиента: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    return None