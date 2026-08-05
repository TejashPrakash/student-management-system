from contextlib import contextmanager

import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG

def connect_database():
    
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        
        if connection.is_connected():
            print("Connected successfully to EduTrack database.")
            return connection
        return None
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


@contextmanager
def db_cursor(dictionary=False, commit=False):
    """Yield a cursor, handling connection setup, commit/rollback and cleanup.

    Raises ConnectionError when the database is unavailable. When ``commit`` is
    True the transaction is committed on success and rolled back on error.
    """
    connection = connect_database()
    if connection is None:
        raise ConnectionError("Database connection unavailable.")

    cursor = connection.cursor(dictionary=dictionary)
    try:
        yield cursor
        if commit:
            connection.commit()
    except Exception:
        if commit:
            connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    test_conn = connect_database()
    if test_conn:
        test_conn.close()
        print("Test connection closed cleanly.")