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
