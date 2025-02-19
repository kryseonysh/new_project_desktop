#analytics.py
import psycopg2
from db import connect_db

def add_analytics(report_start, report_finish):
    """Add a new analytics report to the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO analytics (report_start, report_finish)
                VALUES (%s, %s);
            """, (report_start, report_finish))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка добавления отчета аналитики: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def get_all_analytics():
    """Fetch all analytics reports from the database."""
    conn = connect_db()
    reports = []
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM analytics;")
            reports = cursor.fetchall()
        except Exception as e:
            print(f"Ошибка прочтения отчетов аналитики: {e}")
        finally:
            cursor.close()
            conn.close()
    return reports

def update_analytics_field(report_id, field_name, new_value):
    """Update a specific field of an analytics report in the database."""
    valid_fields = ['report_start', 'report_finish']
    
    if field_name not in valid_fields:
        raise ValueError(f"Invalid field name: {field_name}. Valid fields are: {valid_fields}")

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            query = f"UPDATE analytics SET {field_name} = %s WHERE report_Id = %s;"
            cursor.execute(query, (new_value, report_id))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка изменения информации отчета аналитики: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def delete_analytics(report_id):
    """Delete an analytics report from the database."""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM analytics WHERE report_Id = %s;", (report_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Ошибка удаления отчета аналитики: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    return False

def sales_summary():
    """Return a summary of sales data from the database"""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM sales_summary;")
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Ошибка получения данных о продажах: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
        return []

def transport_order_count():
    """Return the count of transport orders from the database"""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM transport_order_count;")
            rows = cursor.fetchall()
            return rows
        except Exception as e:
            print(f"Ошибка получения данных о заказах транспорта: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
        return []