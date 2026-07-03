import pytest
from shared.utils.json import load_json, save_json, parse_json, JSONError


def test_save_and_load_json(tmp_path):
    file_path = tmp_path / "data.json"
    data = {"key": "value", "number": 42}
    save_json(file_path, data)

    loaded = load_json(file_path)
    assert loaded == data


def test_parse_json():
    data = parse_json('{"test": true}')
    assert data["test"] is True

    with pytest.raises(JSONError):
        parse_json("invalid json")
