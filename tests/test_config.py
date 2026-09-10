import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from config import get_db_config
from errors import ConfigurationError


class GetDbConfigTests(unittest.TestCase):
    def test_raises_when_password_is_missing(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ConfigurationError):
                get_db_config()

    def test_allows_empty_password_when_explicitly_opted_in(self):
        env = {"EDUTRACK_ALLOW_EMPTY_PASSWORD": "1"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(get_db_config()["password"], "")

    def test_invalid_port_raises_a_configuration_error(self):
        env = {"EDUTRACK_DB_PASSWORD": "s3cret", "EDUTRACK_DB_PORT": "not-a-port"}
        with mock.patch.dict(os.environ, env, clear=True):
            with self.assertRaisesRegex(ConfigurationError, "EDUTRACK_DB_PORT"):
                get_db_config()

    def test_reads_settings_from_environment(self):
        env = {
            "EDUTRACK_DB_HOST": "db.internal",
            "EDUTRACK_DB_USER": "edutrack_app",
            "EDUTRACK_DB_PASSWORD": "s3cret",
            "EDUTRACK_DB_NAME": "edutrack_prod",
            "EDUTRACK_DB_PORT": "3307",
            "EDUTRACK_DB_SSL_CA": "/etc/ssl/ca.pem",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            config = get_db_config()

        self.assertEqual(config["host"], "db.internal")
        self.assertEqual(config["user"], "edutrack_app")
        self.assertEqual(config["port"], 3307)
        self.assertEqual(config["ssl_ca"], "/etc/ssl/ca.pem")
        self.assertTrue(config["ssl_verify_identity"])


if __name__ == "__main__":
    unittest.main()
