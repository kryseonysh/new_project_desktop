#transport.py
import psycopg2
from db import connect_db

def add_transport(transport, tclass):
    """Add a new transport record to the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO transport (transport, class)
                VALUES (%s, %s);
            """, (transport, tclass))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка добавления транспорта: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_all_transport():
    """Fetch all transport records from the database."""
    conn = connect_db()
    transport_list = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM transport;")
            transport_list = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка прочтения транспорта: {e}")
        finally:
            cursor.close()
            conn.close()
    return transport_list

def update_transport_field(transport_id, field_name, new_value):
    """Update a specific field of a transport record in the database."""
    valid_fields = ['transport', 'class']
    
    if field_name not in valid_fields:
        raise ValueError(f"Invalid field name: {field_name}. Valid fields are: {valid_fields}")

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = f"UPDATE transport SET {field_name} = %s WHERE transport_Id = %s;"
            cursor.execute(query, (new_value, transport_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка обновления информации о транспорте: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def delete_transport(transport_Id):
    """Delete a transport record from the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM transport WHERE transport_Id = %s;", (transport_Id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка удаления транспорта: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False