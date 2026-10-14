import os
import mysql.connector
from mysql.connector import Error

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "todo_db")


def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )


def test_connection():
    connection = None
    try:
        connection = get_connection()
        if connection.is_connected():
            db_info = connection.get_server_info()
            return True, f"Connected to MySQL Server version {db_info}"
        return False, "Failed to connect to MySQL."
    except Error as err:
        return False, str(err)
    finally:
        if connection is not None and connection.is_connected():
            connection.close()


def get_all_tasks():
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, title, description, status, created_at FROM tasks ORDER BY id ASC;"
        cursor.execute(query)
        tasks = cursor.fetchall()
        return tasks
    except Error as err:
        print(f"[Database Error] Could not retrieve tasks: {err}")
        return []
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def get_task_by_id(task_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT id, title, description, status, created_at FROM tasks WHERE id = %s;"
        cursor.execute(query, (task_id,))
        task = cursor.fetchone()
        return task
    except Error as err:
        print(f"[Database Error] Could not retrieve task #{task_id}: {err}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def insert_task(title, description=None):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "INSERT INTO tasks (title, description, status) VALUES (%s, %s, %s);"
        cursor.execute(query, (title, description, "Pending"))
        connection.commit()
        return cursor.lastrowid
    except Error as err:
        if connection is not None:
            connection.rollback()
        print(f"[Database Error] Could not insert task: {err}")
        return None
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def update_task(task_id, title, description=None):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE tasks SET title = %s, description = %s WHERE id = %s;"
        cursor.execute(query, (title, description, task_id))
        connection.commit()
        return cursor.rowcount > 0
    except Error as err:
        if connection is not None:
            connection.rollback()
        print(f"[Database Error] Could not update task #{task_id}: {err}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def mark_task_status(task_id, status="Completed"):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "UPDATE tasks SET status = %s WHERE id = %s;"
        cursor.execute(query, (status, task_id))
        connection.commit()
        return cursor.rowcount > 0
    except Error as err:
        if connection is not None:
            connection.rollback()
        print(f"[Database Error] Could not update status for task #{task_id}: {err}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


def delete_task(task_id):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = "DELETE FROM tasks WHERE id = %s;"
        cursor.execute(query, (task_id,))
        connection.commit()
        return cursor.rowcount > 0
    except Error as err:
        if connection is not None:
            connection.rollback()
        print(f"[Database Error] Could not delete task #{task_id}: {err}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
