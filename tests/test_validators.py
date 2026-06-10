"""
tests/test_validators.py
------------------------
Unit tests for utils/validators.py.
These tests require no database connection and run offline.

Run with:
    pytest tests/test_validators.py -v
"""

import pytest
from utils.validators import (
    is_non_empty,
    is_valid_email,
    is_min_length,
    parse_int,
    parse_float,
)


class TestIsNonEmpty:
    def test_valid_string(self):
        ok, err = is_non_empty("hello")
        assert ok is True
        assert err == ""

    def test_empty_string(self):
        ok, err = is_non_empty("")
        assert ok is False
        assert err != ""

    def test_whitespace_only(self):
        ok, err = is_non_empty("   ")
        assert ok is False

    def test_custom_field_name_in_error(self):
        _, err = is_non_empty("", "Username")
        assert "Username" in err


class TestIsValidEmail:
    def test_valid_emails(self):
        for email in ["user@example.com", "a.b+c@mail.org", "x@y.co.uk"]:
            ok, _ = is_valid_email(email)
            assert ok is True, f"Expected valid: {email}"

    def test_invalid_emails(self):
        for email in ["notanemail", "missing@", "@nodomain.com", "no at sign"]:
            ok, _ = is_valid_email(email)
            assert ok is False, f"Expected invalid: {email}"


class TestIsMinLength:
    def test_meets_minimum(self):
        ok, _ = is_min_length("abcdef", 6)
        assert ok is True

    def test_below_minimum(self):
        ok, err = is_min_length("abc", 6, "Password")
        assert ok is False
        assert "Password" in err

    def test_exactly_minimum(self):
        ok, _ = is_min_length("abcde", 5)
        assert ok is True


class TestParseInt:
    def test_valid_integer(self):
        val, err = parse_int("5")
        assert val == 5
        assert err == ""

    def test_zero_is_invalid(self):
        val, err = parse_int("0")
        assert val is None
        assert err != ""

    def test_negative_is_invalid(self):
        val, err = parse_int("-3")
        assert val is None

    def test_non_numeric(self):
        val, err = parse_int("abc")
        assert val is None
        assert err != ""

    def test_whitespace_stripped(self):
        val, _ = parse_int("  7  ")
        assert val == 7


class TestParseFloat:
    def test_valid_float(self):
        val, err = parse_float("9.99")
        assert val == pytest.approx(9.99)
        assert err == ""

    def test_integer_string_accepted(self):
        val, _ = parse_float("10")
        assert val == pytest.approx(10.0)

    def test_zero_is_invalid(self):
        val, err = parse_float("0")
        assert val is None

    def test_negative_is_invalid(self):
        val, _ = parse_float("-5.0")
        assert val is None

    def test_non_numeric(self):
        val, err = parse_float("xyz")
        assert val is None
        assert err != ""
