"""Small, reusable helpers for validating console input."""

import re
from datetime import date, datetime

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s.]+(\.[^@\s.]+)+$")
PHONE_PATTERN = re.compile(r"^\+?[0-9][0-9 \-]{5,19}$")
GENDERS = ("Male", "Female", "Other")


def get_positive_int(prompt: str, input_fn=input, output_fn=print) -> int:
    """Keep prompting until the user enters a positive whole number."""
    while True:
        raw_value = input_fn(prompt).strip()
        try:
            value = int(raw_value)
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            output_fn("Please enter a positive whole number.")


def get_text(prompt: str, max_length: int, input_fn=input, output_fn=print, min_length: int = 1) -> str:
    """Prompt until a non-empty value within the column length limit is given."""
    while True:
        value = input_fn(prompt).strip()
        if len(value) < min_length:
            output_fn("This field is required.")
        elif len(value) > max_length:
            output_fn(f"Please use at most {max_length} characters.")
        else:
            return value


def get_choice(prompt: str, choices=GENDERS, input_fn=input, output_fn=print) -> str:
    """Prompt until the value matches one of the allowed choices (case-insensitive)."""
    lookup = {choice.lower(): choice for choice in choices}
    while True:
        value = input_fn(prompt).strip().lower()
        if value in lookup:
            return lookup[value]
        output_fn(f"Please enter one of: {', '.join(choices)}.")


def get_date(prompt: str, input_fn=input, output_fn=print, allow_future: bool = True) -> str:
    """Prompt until a valid YYYY-MM-DD date is given and return it normalised."""
    while True:
        raw_value = input_fn(prompt).strip()
        try:
            parsed = datetime.strptime(raw_value, "%Y-%m-%d").date()
        except ValueError:
            output_fn("Please enter a date in YYYY-MM-DD format.")
            continue
        if not allow_future and parsed > date.today():
            output_fn("The date cannot be in the future.")
            continue
        return parsed.isoformat()


def get_email(prompt: str, input_fn=input, output_fn=print, max_length: int = 255) -> str:
    """Prompt until a plausible email address is given."""
    while True:
        value = input_fn(prompt).strip()
        if len(value) <= max_length and EMAIL_PATTERN.match(value):
            return value
        output_fn("Please enter a valid email address.")


def get_phone(prompt: str, input_fn=input, output_fn=print, max_length: int = 20) -> str:
    """Prompt until a plausible phone number is given."""
    while True:
        value = input_fn(prompt).strip()
        if len(value) <= max_length and PHONE_PATTERN.match(value):
            return value
        output_fn("Please enter a valid phone number (digits, spaces and dashes only).")
