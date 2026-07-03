from backend.services.security.input_validator import InputValidator


def test_sql_injection_prevention():
    """
    Verifies that basic SQL injection patterns are caught.
    """
    validator = InputValidator()

    # Valid input
    assert validator.validate_string("My Cafe") == True

    # Invalid input
    assert validator.validate_string("My Cafe; DROP TABLE business;") == False
    assert validator.validate_string("SELECT * FROM users") == False
    assert validator.validate_string("name -- comment") == False
