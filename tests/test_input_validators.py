import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from input_validators import get_positive_int


class GetPositiveIntTests(unittest.TestCase):
    def test_returns_a_valid_positive_integer(self):
        self.assertEqual(get_positive_int("Roll: ", lambda _: "42"), 42)

    def test_reprompts_after_invalid_values(self):
        values = iter(["abc", "0", "-3", "7"])
        messages = []

        result = get_positive_int("Roll: ", lambda _: next(values), messages.append)

        self.assertEqual(result, 7)
        self.assertEqual(messages, ["Please enter a positive whole number."] * 3)


if __name__ == "__main__":
    unittest.main()
