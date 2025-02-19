#orders.py
import psycopg2
from db import connect_db

def add_order(client_id, route_id, order_status, payment_method, discount_id, cost, transport_id, hotel_id):
    """Add a new order to the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT add_order(%s, %s, %s, %s, %s, %s, %s, %s);
            """, (client_id, route_id, order_status, payment_method, discount_id, cost, transport_id, hotel_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка добавления заказа: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_all_orders():
    """Fetch all orders from the database."""
    conn = connect_db()
    orders = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM orders;")
            orders = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка прочтения заказов: {e}")
        finally:
            cursor.close()
            conn.close()
    return orders

def update_order_field(order_id, field_name, new_value):
    """Update a specific field of an order in the database."""
    valid_fields = ['client_Id', 'route_Id', 'order_status', 'payment_method', 'discount_Id', 'cost', 'transport_Id', 'hotel_Id']
    
    if field_name not in valid_fields:
        raise ValueError(f"Invalid field name: {field_name}. Valid fields are: {valid_fields}")

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = f"UPDATE orders SET {field_name} = %s WHERE order_Id = %s;"
            cursor.execute(query, (new_value, order_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка изменения информации о заказе: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def delete_order(order_id):
    """Delete an order from the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM orders WHERE order_Id = %s;", (order_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка удаления заказа: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def update_order_status(order_id,  new_status):
    """Update the status of an order in the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                'CALL update_order_status(%s, %s)',
                (order_id,  new_status)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка изменения статуса заказа: {e}")
            return False
        
def get_client_orders():
    """Get all orders with full name of client from the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM client_orders;")
            orders = cursor.fetchall()
            return orders
        except Exception as e:
            print(f"Ошибка прочтения заказов: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []