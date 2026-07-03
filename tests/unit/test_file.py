from shared.utils.file import read_text, write_text, file_exists, safe_delete


def test_write_and_read_text(tmp_path):
    file_path = tmp_path / "test.txt"
    write_text(file_path, "hello world")
    assert file_exists(file_path)
    assert read_text(file_path) == "hello world"


def test_safe_delete(tmp_path):
    file_path = tmp_path / "delete_me.txt"
    write_text(file_path, "to delete")
    assert file_exists(file_path)

    assert safe_delete(file_path) is True
    assert not file_exists(file_path)
    assert safe_delete(file_path) is False
