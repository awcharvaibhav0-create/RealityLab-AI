import pytest
from shared.utils.validation import (
    require_not_none,
    require_non_empty_string,
    require_in_range,
    require_positive,
    ValidationError,
)


def test_require_not_none():
    assert require_not_none("test") == "test"
    with pytest.raises(ValidationError):
        require_not_none(None)


def test_require_non_empty_string():
    assert require_non_empty_string("hello") == "hello"
    with pytest.raises(ValidationError):
        require_non_empty_string("")
    with pytest.raises(ValidationError):
        require_non_empty_string("   ")
    with pytest.raises(ValidationError):
        require_non_empty_string(123)


def test_require_in_range():
    assert require_in_range(5, 1, 10) == 5
    with pytest.raises(ValidationError):
        require_in_range(0, 1, 10)


def test_require_positive():
    assert require_positive(10) == 10
    with pytest.raises(ValidationError):
        require_positive(0)
