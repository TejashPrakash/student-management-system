import os

from errors import ConfigurationError


def get_db_config():
    raw_port = os.getenv("EDUTRACK_DB_PORT", "3306")
    try:
        port = int(raw_port)
    except ValueError as exc:
        raise ConfigurationError(
            f"EDUTRACK_DB_PORT must be an integer, got {raw_port!r}."
        ) from exc

    return {
        "host": os.getenv("EDUTRACK_DB_HOST", "localhost"),
        "user": os.getenv("EDUTRACK_DB_USER", "root"),
        "password": os.getenv("EDUTRACK_DB_PASSWORD", ""),
        "database": os.getenv("EDUTRACK_DB_NAME", "edutrack"),
        "port": port,
    }
