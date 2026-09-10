import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import database
from errors import ConfigurationError, DatabaseConnectionError
from mysql.connector import Error


FAKE_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "pw",
    "database": "edutrack",
    "port": 3306,
}


class ConnectDatabaseTests(unittest.TestCase):
    def test_returns_connection_when_connected(self):
        fake_conn = mock.Mock()
        fake_conn.is_connected.return_value = True

        with mock.patch.object(database, "get_db_config", return_value=FAKE_CONFIG), \
                mock.patch.object(
                    database.mysql.connector, "connect", return_value=fake_conn
                ) as connect:
            result = database.connect_database()

        self.assertIs(result, fake_conn)
        connect.assert_called_once_with(**FAKE_CONFIG)

    def test_raises_and_closes_when_not_connected(self):
        fake_conn = mock.Mock()
        fake_conn.is_connected.return_value = False

        with mock.patch.object(database, "get_db_config", return_value=FAKE_CONFIG), \
                mock.patch.object(
                    database.mysql.connector, "connect", return_value=fake_conn
                ):
            with self.assertRaises(DatabaseConnectionError):
                database.connect_database()

        fake_conn.close.assert_called_once()

    def test_wraps_connector_error(self):
        with mock.patch.object(database, "get_db_config", return_value=FAKE_CONFIG), \
                mock.patch.object(
                    database.mysql.connector, "connect", side_effect=Error("boom")
                ):
            with self.assertRaises(DatabaseConnectionError):
                database.connect_database()

    def test_propagates_configuration_error(self):
        with mock.patch.object(
            database, "get_db_config", side_effect=ConfigurationError("missing password")
        ):
            with self.assertRaises(ConfigurationError):
                database.connect_database()


class CloseQuietlyTests(unittest.TestCase):
    def test_none_is_a_noop(self):
        self.assertIsNone(database.close_quietly(None))

    def test_closes_resource(self):
        resource = mock.Mock()
        database.close_quietly(resource)
        resource.close.assert_called_once()

    def test_swallows_close_error(self):
        resource = mock.Mock()
        resource.close.side_effect = Error("cannot close")
        self.assertIsNone(database.close_quietly(resource))


if __name__ == "__main__":
    unittest.main()
