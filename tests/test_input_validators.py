import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from input_validators import (
    get_choice,
    get_date,
    get_email,
    get_phone,
    get_positive_int,
    get_text,
)


class GetPositiveIntTests(unittest.TestCase):
    def test_returns_a_valid_positive_integer(self):
        self.assertEqual(get_positive_int("Roll: ", lambda _: "42"), 42)

    def test_reprompts_after_invalid_values(self):
        values = iter(["abc", "0", "-3", "7"])
        messages = []

        result = get_positive_int("Roll: ", lambda _: next(values), messages.append)

        self.assertEqual(result, 7)
        self.assertEqual(messages, ["Please enter a positive whole number."] * 3)


class GetTextTests(unittest.TestCase):
    def test_rejects_empty_and_oversized_values(self):
        values = iter(["", "x" * 51, "Aanya"])
        messages = []

        result = get_text("Name: ", 50, lambda _: next(values), messages.append)

        self.assertEqual(result, "Aanya")
        self.assertEqual(len(messages), 2)


class GetChoiceTests(unittest.TestCase):
    def test_normalises_case_and_rejects_unknown_values(self):
        values = iter(["dog", "female"])
        messages = []

        result = get_choice("Gender: ", input_fn=lambda _: next(values), output_fn=messages.append)

        self.assertEqual(result, "Female")
        self.assertEqual(len(messages), 1)


class GetDateTests(unittest.TestCase):
    def test_rejects_malformed_dates(self):
        values = iter(["2020-13-01", "01/02/2020", "2020-02-29"])
        messages = []

        result = get_date("DOB: ", lambda _: next(values), messages.append)

        self.assertEqual(result, "2020-02-29")
        self.assertEqual(len(messages), 2)

    def test_rejects_future_dates_when_disallowed(self):
        values = iter(["2999-01-01", "2000-01-01"])
        messages = []

        result = get_date("DOB: ", lambda _: next(values), messages.append, allow_future=False)

        self.assertEqual(result, "2000-01-01")
        self.assertEqual(messages, ["The date cannot be in the future."])


class GetEmailTests(unittest.TestCase):
    def test_rejects_malformed_addresses(self):
        values = iter(["not-an-email", "a@b", "aanya@example.com"])
        messages = []

        result = get_email("Email: ", lambda _: next(values), messages.append)

        self.assertEqual(result, "aanya@example.com")
        self.assertEqual(len(messages), 2)


class GetPhoneTests(unittest.TestCase):
    def test_rejects_malformed_numbers(self):
        values = iter(["12", "call me", "+91 98765-43210"])
        messages = []

        result = get_phone("Phone: ", lambda _: next(values), messages.append)

        self.assertEqual(result, "+91 98765-43210")
        self.assertEqual(len(messages), 2)


if __name__ == "__main__":
    unittest.main()
