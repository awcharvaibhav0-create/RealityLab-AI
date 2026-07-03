from pathlib import Path
from typing import Union


def read_text(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """Read text from a file safely."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {path}")
    return path.read_text(encoding=encoding)


def write_text(
    file_path: Union[str, Path],
    content: str,
    encoding: str = "utf-8",
    overwrite: bool = True,
) -> None:
    """Write text to a file safely."""
    path = Path(file_path)
    if not overwrite and path.exists():
        raise FileExistsError(f"File already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding=encoding)


def file_exists(file_path: Union[str, Path]) -> bool:
    """Check if a file exists."""
    return Path(file_path).is_file()


def safe_delete(file_path: Union[str, Path]) -> bool:
    """Delete a file safely, returning True if successful."""
    path = Path(file_path)
    if path.is_file():
        try:
            path.unlink()
            return True
        except OSError:
            return False
    return False
