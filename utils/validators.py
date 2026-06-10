"""
utils/validators.py
--------------------
Pure-function helpers for validating and sanitising user input.
None of these functions interact with the database or produce I/O.
"""

import re


# ---------------------------------------------------------------------------
# String checks
# ---------------------------------------------------------------------------

def is_non_empty(value: str, field_name: str = "Field") -> tuple[bool, str]:
    """Return (True, '') when the value is a non-blank string."""
    if not value or not value.strip():
        return False, f"{field_name} cannot be empty."
    return True, ""


def is_valid_email(email: str) -> tuple[bool, str]:
    """Basic e-mail format check."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email.strip()):
        return False, "Invalid email format. Example: user@example.com"
    return True, ""


def is_min_length(value: str, min_len: int, field_name: str = "Field") -> tuple[bool, str]:
    """Check that a string meets a minimum character length."""
    if len(value.strip()) < min_len:
        return False, f"{field_name} must be at least {min_len} characters long."
    return True, ""


# ---------------------------------------------------------------------------
# Numeric parsing
# ---------------------------------------------------------------------------

def parse_int(raw: str, field_name: str = "Value") -> tuple[int | None, str]:
    """
    Parse *raw* as a positive integer.
    Returns (int, '') on success or (None, error_message) on failure.
    """
    try:
        value = int(raw.strip())
        if value <= 0:
            return None, f"{field_name} must be a positive integer."
        return value, ""
    except ValueError:
        return None, f"{field_name} must be a whole number (e.g. 3)."


def parse_float(raw: str, field_name: str = "Value") -> tuple[float | None, str]:
    """
    Parse *raw* as a positive float.
    Returns (float, '') on success or (None, error_message) on failure.
    """
    try:
        value = float(raw.strip())
        if value <= 0:
            return None, f"{field_name} must be a positive number."
        return value, ""
    except ValueError:
        return None, f"{field_name} must be a number (e.g. 49.99)."
