from datetime import datetime

import pytest
from pytz import timezone

from app.validators import (
    is_country_code,
    is_rating,
    is_tz_aware,
    no_whitespace,
    not_empty,
)


# ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("string, passes"),
    [("", False), ("emptystring", True)],
)
def test_not_empty(string, passes):
    if not passes:
        with pytest.raises(ValueError):
            not_empty(string)
    else:
        result = not_empty(string)
        assert result == string


# ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("string, passes"),
    [
        ("", True),
        ("mrswhitespace", True),
        (" ", False),
        ("\t", False),
        ("\r", False),
        ("\n", False),
        ("\v", False),
        ("\f", False),
        ("  ", False),
        ("\t\t", False),
        ("\r\r", False),
        ("\n\n", False),
        ("\v\v", False),
        ("\f\f", False),
        ("mrs whitespace", False),
        ("mrs\twhitespace", False),
        ("mrs\rwhitespace", False),
        ("mrs\nwhitespace", False),
        ("mrs\vwhitespace", False),
        ("mrs\fwhitespace", False),
    ],
)
def test_no_whitespace(string, passes):
    if not passes:
        with pytest.raises(ValueError):
            no_whitespace(string)
    else:
        result = no_whitespace(string)
        assert result == string


# ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("timestamp, passes"),
    [
        (datetime(2021, 8, 17), False),
        (datetime(2021, 8, 17, tzinfo=timezone("UTC")), True),
        (datetime(2021, 8, 17, tzinfo=timezone("Europe/Berlin")), True),
    ],
)
def test_is_tz_aware(timestamp, passes):
    if not passes:
        with pytest.raises(ValueError):
            is_tz_aware(timestamp)
    else:
        result = is_tz_aware(timestamp)
        assert result == timestamp


# ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("timestamp, passes"),
    [
        ("XYZ", False),
        ("EN", False),
        ("DE", True),
        ("ES", True),
    ],
)
def test_is_country_code(timestamp, passes):
    if not passes:
        with pytest.raises(ValueError):
            is_country_code(timestamp)
    else:
        result = is_country_code(timestamp)
        assert result == timestamp


# ---------------------------------------------------------------------
@pytest.mark.parametrize(
    ("rating, passes"),
    [
        (-1, False),
        (11, False),
        (1, True),
        (3, True),
        (5, True),
        (8, True),
        (0, True),
    ],
)
def test_is_rating(rating, passes):
    if not passes:
        with pytest.raises(ValueError):
            is_rating(rating)
    else:
        result = is_rating(rating)
        assert result == rating
