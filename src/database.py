import logging

import mysql.connector
from mysql.connector import Error

from config import get_db_config
from errors import DatabaseConnectionError

logger = logging.getLogger(__name__)


def connect_database():
    """Open a MySQL connection.

    Raises:
        ConfigurationError: the database configuration is invalid.
        DatabaseConnectionError: the connection could not be established.
    """
    config = get_db_config()
    try:
        connection = mysql.connector.connect(**config)
    except Error as exc:
        raise DatabaseConnectionError(
            f"Could not connect to MySQL at {config['host']}:{config['port']}: {exc}"
        ) from exc

    if not connection.is_connected():
        connection.close()
        raise DatabaseConnectionError(
            f"MySQL at {config['host']}:{config['port']} accepted the connection "
            "but reported it as closed."
        )

    logger.info("Connected successfully to EduTrack database.")
    return connection


def close_quietly(resource):
    """Close a cursor or connection, logging (never raising) on failure."""
    if resource is None:
        return
    try:
        resource.close()
    except Error:
        logger.warning("Failed to close %r cleanly.", resource, exc_info=True)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    test_conn = connect_database()
    close_quietly(test_conn)
    logger.info("Test connection closed cleanly.")
