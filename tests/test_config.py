import importlib
import os
import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import config


class GetDbConfigTests(unittest.TestCase):
    def test_uses_defaults_when_env_missing(self):
        with mock.patch.dict(os.environ, {}, clear=True):
            cfg = config.get_db_config()
        self.assertEqual(
            cfg,
            {
                "host": "localhost",
                "user": "root",
                "password": "",
                "database": "edutrack",
                "port": 3306,
            },
        )

    def test_reads_values_from_environment(self):
        env = {
            "EDUTRACK_DB_HOST": "db.example.com",
            "EDUTRACK_DB_USER": "admin",
            "EDUTRACK_DB_PASSWORD": "secret",
            "EDUTRACK_DB_NAME": "school",
            "EDUTRACK_DB_PORT": "5432",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            cfg = config.get_db_config()
        self.assertEqual(cfg["host"], "db.example.com")
        self.assertEqual(cfg["user"], "admin")
        self.assertEqual(cfg["password"], "secret")
        self.assertEqual(cfg["database"], "school")
        self.assertEqual(cfg["port"], 5432)

    def test_port_is_coerced_to_int(self):
        with mock.patch.dict(os.environ, {"EDUTRACK_DB_PORT": "3307"}, clear=True):
            cfg = config.get_db_config()
        self.assertIsInstance(cfg["port"], int)
        self.assertEqual(cfg["port"], 3307)


class DbConfigConstantTests(unittest.TestCase):
    def test_module_level_constant_reflects_environment_at_import(self):
        env = {"EDUTRACK_DB_NAME": "reloaded_db"}
        with mock.patch.dict(os.environ, env, clear=True):
            reloaded = importlib.reload(config)
            self.assertEqual(reloaded.DB_CONFIG["database"], "reloaded_db")
        # restore module state for other tests
        importlib.reload(config)


if __name__ == "__main__":
    unittest.main()
