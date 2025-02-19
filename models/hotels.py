#hotels.py
import psycopg2
from db import connect_db

def add_hotel(star, room_class, bedding):
    """Add a new hotel to the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO hotels (star, room_class, bedding)
                VALUES (%s, %s, %s);
            """, (star, room_class, bedding))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка добавления отеля: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_all_hotels():
    """Fetch all hotels from the database."""
    conn = connect_db()
    hotels = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM hotels;")
            hotels = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка прочтения отелей: {e}")
        finally:
            cursor.close()
            conn.close()
    return hotels


def update_hotel_field(hotel_id, field_name, new_value):
    """Update a specific field of a hotel in the database."""
    valid_fields = ['star', 'room_class', 'bedding']
    
    if field_name not in valid_fields:
        raise ValueError(f"Invalid field name: {field_name}. Valid fields are: {valid_fields}")

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = f"UPDATE hotels SET {field_name} = %s WHERE hotel_Id = %s;"
            cursor.execute(query, (new_value, hotel_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка изменения информации об отеле: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def delete_hotel(hotel_id):
    """Delete a hotel from the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM hotels WHERE hotel_Id = %s;", (hotel_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка удаления отеля: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False