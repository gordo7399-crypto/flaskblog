import pytest
from wtforms.validators import ValidationError
from flaskblog.forms import validate_password_strength

@pytest.mark.parametrize("valid_pwd", [
    "testing1",
    "thisisaPassword1",
    "12345678",
])
def test_valid_passwords(valid_pwd):
    """Verifies that compliant passwords pass validtion without raising an error."""
    assert validate_password_strength(valid_pwd) is True

@pytest.mark.parametrize("invalid_pwd, expected_error_msg", [
    ("pass1", "at least 8 characters"),
    ("password", "at least one number"),
    ("short", "at least 8 characters" ),
    ("", "at least 8 characters"), 
])
def test_invalid_passwords(invalid_pwd, expected_error_msg):
    """Verifies that weak passwords trigger a ValidationError with the correct message."""
    with pytest.raises(ValidationError) as exc_info:
        validate_password_strength(invalid_pwd)
    
    assert expected_error_msg in str(exc_info.value)