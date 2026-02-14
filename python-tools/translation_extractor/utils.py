import re
from pathlib import Path


def to_camel_case(name):
    """Convert string to camelCase"""
    words = name.split()
    if not words:
        return ""
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])


def to_pascal_case(name):
    """Convert string to PascalCase"""
    words = name.split()
    return ''.join(word.capitalize() for word in words)


def to_snake_case(name):
    """Convert string to snake_case"""
    words = name.split()
    if not words:
        return ""
    return '_'.join(word.lower() for word in words)


def to_kebab_case(name):
    """Convert string to kebab-case"""
    words = name.split()
    if not words:
        return ""
    return '-'.join(word.lower() for word in words)


def suggest_translation_key(text: str) -> str:
    """Suggest a translation key based on text content"""
    # Remove special characters and normalize
    text = re.sub(r'[^\w\s]', '', text)
    # Convert to camelCase for key suggestion
    return to_camel_case(text) if text else "key"


def get_code_files(directory: Path, extensions: tuple = ('.ts', '.tsx', '.js', '.jsx')) -> list:
    """Get all code files from directory recursively"""
    files = []
    for ext in extensions:
        files.extend(directory.rglob(f'*{ext}'))
    return files


def load_json_file(file_path: Path) -> dict:
    """Load JSON file and return dict, return empty dict on error"""
    import json
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_json_file(file_path: Path, data: dict, indent: int = 2) -> bool:
    """Save dict to JSON file, return True on success"""
    import json
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        return True
    except Exception:
        return False


def get_nested_value(data: dict, key_path: str, default=None):
    """Get nested value from dict using dot notation (e.g., 'form.name')"""
    keys = key_path.split('.')
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current


def set_nested_value(data: dict, key_path: str, value):
    """Set nested value in dict using dot notation (e.g., 'form.name')"""
    keys = key_path.split('.')
    current = data
    for i, key in enumerate(keys[:-1]):
        if key not in current or not isinstance(current[key], dict):
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value


def get_all_keys(data: dict, prefix: str = '') -> set:
    """Get all keys from nested dict as dot-notation strings"""
    keys = set()
    for key, value in data.items():
        full_key = f"{prefix}.{key}" if prefix else key
        if isinstance(value, dict):
            keys.update(get_all_keys(value, full_key))
        else:
            keys.add(full_key)
    return keys
