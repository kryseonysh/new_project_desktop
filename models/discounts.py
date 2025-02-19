#discounts.py
import psycopg2
from db import connect_db

def add_discount(discount_description, rate, startdate, finishdate):
    """Add a new discount to the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO discounts (discount_description, rate, startdate, finishdate)
                VALUES (%s, %s, %s, %s);
            """, (discount_description, rate, startdate, finishdate))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка добавления скидки: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_all_discounts():
    """Fetch all discounts from the database."""
    conn = connect_db()
    discounts = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM discounts;")
            discounts = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка прочтения скидки: {e}")
        finally:
            cursor.close()
            conn.close()
    return discounts


def update_discount_field(discount_id, field_name, new_value):
    """Update a specific field of a discount in the database."""
    valid_fields = ['discount_description', 'rate', 'startdate', 'finishdate']
    
    if field_name not in valid_fields:
        raise ValueError(f"Invalid field name: {field_name}. Valid fields are: {valid_fields}")

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = f"UPDATE discounts SET {field_name} = %s WHERE discount_Id = %s;"
            cursor.execute(query, (new_value, discount_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка обновления информации о скидке: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def delete_discount(discount_id):
    """Delete a discount from the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM discounts WHERE discount_Id = %s;", (discount_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка удаления скидки: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def active_discounts():
    """Get all active discounts from the database"""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM active_discounts;")
            active_discounts = cursor.fetchall()
            return active_discounts
        except Exception as e:
            print(f"Ошибка получения активных скидок: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
            return []