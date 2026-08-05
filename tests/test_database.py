import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import database
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

    def test_returns_none_when_not_connected(self):
        fake_conn = mock.Mock()
        fake_conn.is_connected.return_value = False

        with mock.patch.object(database, "get_db_config", return_value=FAKE_CONFIG), \
                mock.patch.object(
                    database.mysql.connector, "connect", return_value=fake_conn
                ):
            result = database.connect_database()

        self.assertIsNone(result)

    def test_returns_none_and_swallows_connection_error(self):
        with mock.patch.object(database, "get_db_config", return_value=FAKE_CONFIG), \
                mock.patch.object(
                    database.mysql.connector, "connect", side_effect=Error("boom")
                ):
            result = database.connect_database()

        self.assertIsNone(result)

    def test_returns_none_on_configuration_error(self):
        with mock.patch.object(
            database, "get_db_config", side_effect=RuntimeError("missing password")
        ):
            result = database.connect_database()

        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
