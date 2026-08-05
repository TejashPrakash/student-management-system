import os

def get_db_config():

    return {
        "host": os.getenv("EDUTRACK_DB_HOST", "localhost"),
        "user": os.getenv("EDUTRACK_DB_USER", "root"),
        "password": os.getenv("EDUTRACK_DB_PASSWORD", ""),
        "database": os.getenv("EDUTRACK_DB_NAME", "edutrack"),
        "port": int(os.getenv("EDUTRACK_DB_PORT", 3306)),
    }
