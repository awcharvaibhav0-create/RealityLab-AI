import json
from pathlib import Path
from typing import Any, Dict, Union


class JSONError(Exception):
    """Base exception for JSON operations."""

    pass


def load_json(file_path: Union[str, Path]) -> Dict[str, Any]:
    """Load and parse a JSON file."""
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"JSON file not found: {path}")

    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise JSONError(f"Invalid JSON in {path}: {e}")
    except Exception as e:
        raise JSONError(f"Error reading JSON from {path}: {e}")


def save_json(
    file_path: Union[str, Path], data: Any, indent: int = 4, overwrite: bool = True
) -> None:
    """Save data to a JSON file."""
    path = Path(file_path)
    if not overwrite and path.exists():
        raise FileExistsError(f"JSON file already exists: {path}")

    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
    except TypeError as e:
        raise JSONError(f"Object not JSON serializable: {e}")
    except Exception as e:
        raise JSONError(f"Error saving JSON to {path}: {e}")


def parse_json(json_str: str) -> Dict[str, Any]:
    """Parse a JSON string."""
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise JSONError(f"Invalid JSON string: {e}")
