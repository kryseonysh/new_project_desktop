#routes.py
import psycopg2
from db import connect_db

def add_route(route_name, startpoint, endpoint, time_departure, time_arrival):
    """Add a new route to the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO routes (route_name, startpoint, endpoint, time_departure, time_arrival)
                VALUES (%s, %s, %s, %s, %s);
            """, (route_name, startpoint, endpoint, time_departure, time_arrival))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка добавления маршрута: {e}")
            return False 
        finally:
            cursor.close()
            conn.close()
    return False

def get_all_routes():
    """Fetch all routes from the database."""
    conn = connect_db()
    routes = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM routes;")
            routes = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка чтения маршрутов: {e}")
        finally:
            cursor.close()
            conn.close()
    return routes

def update_route_field(route_id, field_name, new_value):
    """Update a specific field of a route in the database."""
    valid_fields = ['route_name', 'startpoint', 'endpoint', 'time_departure', 'time_arrival']
    
    if field_name not in valid_fields:
        raise ValueError(f"Invalid field name: {field_name}. Valid fields are: {valid_fields}")

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = f"UPDATE routes SET {field_name} = %s WHERE route_Id = %s;"
            cursor.execute(query, (new_value, route_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка изменения информации о маршруте: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def delete_route(route_id):
    """Delete a route from the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM routes WHERE route_Id = %s;", (route_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка удаления маршрута: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_routes_by_startpoint(startpoint):
    """Get all routes that start at a specific point."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT * FROM get_routes_by_startpoint(%s);
            """, (startpoint,))
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка получения маршрутов по начальной точке: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    return []

def route_order_count():
    """Get the number of routes in the orders."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM route_order_count;")
            result = cursor.fetchall()
            return result
        except Exception as e:
            print(f"Ошибка получения количества заказов: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
        return [] 