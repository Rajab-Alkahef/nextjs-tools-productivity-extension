"""
Utility functions for string manipulation and URL processing.
"""
import re
from urllib.parse import urlparse


def camel_case(*parts):
    """
    Convert multiple string parts to camelCase, e.g. ("Persons", "Create") -> "personsCreate"
    """
    cleaned = []
    for p in parts:
        if not p:
            continue
        tokens = re.split(r"[^a-zA-Z0-9]+", p)
        tokens = [t for t in tokens if t]
        if not tokens:
            continue
        cleaned.append(tokens)
    if not cleaned:
        return "endpoint"

    flat = [t for part in cleaned for t in part]
    first = flat[0].lower()
    rest = [w.capitalize() for w in flat[1:]]
    return first + "".join(rest)


def split_base_and_path(url):
    """
    Split full URL into (base_url, path_with_leading_slash_plus_query).
    base_url: scheme://host[:port]
    path: '/rest/of/path?query...'
    """
    if not url:
        return "", ""

    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return "", url

    base = f"{parsed.scheme}://{parsed.netloc}"
    path = parsed.path or ""
    if not path.startswith("/"):
        path = "/" + path
    if parsed.query:
        path = path + "?" + parsed.query
    return base, path


def remove_postman_variables(url):
    """
    Remove Postman environment variables like {{trustserviceURL}} from URL.
    """
    if not url:
        return url
    # Remove Postman variables like {{trustserviceURL}}
    url = re.sub(r'\{\{[^}]+\}\}', '', url)
    return url.strip()
