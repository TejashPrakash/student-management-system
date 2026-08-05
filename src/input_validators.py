"""Small, reusable helpers for validating console input."""


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
