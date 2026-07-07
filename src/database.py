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

if __name__ == "__main__":
    test_conn = connect_database()
    if test_conn:
        test_conn.close()
        print("Test connection closed cleanly.")