import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from config import get_db_config
from errors import ConfigurationError


class GetDbConfigTests(unittest.TestCase):
    def test_reads_values_from_the_environment(self):
        with patch.dict("os.environ", {"EDUTRACK_DB_HOST": "db", "EDUTRACK_DB_PORT": "3307"}):
            config = get_db_config()

        self.assertEqual(config["host"], "db")
        self.assertEqual(config["port"], 3307)

    def test_invalid_port_raises_a_configuration_error(self):
        with patch.dict("os.environ", {"EDUTRACK_DB_PORT": "not-a-port"}):
            with self.assertRaisesRegex(ConfigurationError, "EDUTRACK_DB_PORT"):
                get_db_config()


if __name__ == "__main__":
    unittest.main()
