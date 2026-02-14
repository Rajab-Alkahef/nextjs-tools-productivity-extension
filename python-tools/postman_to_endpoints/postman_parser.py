"""
Functions for parsing Postman collection JSON files.
"""
from utils import camel_case


def extract_url(request_obj):
    """
    Safely extract URL string from a Postman request object.
    """
    if not request_obj:
        return None

    url = None
    url_obj = request_obj.get("url")
    if isinstance(url_obj, str):
        url = url_obj
    elif isinstance(url_obj, dict):
        if "raw" in url_obj and isinstance(url_obj["raw"], str):
            url = url_obj["raw"]
        else:
            protocol = url_obj.get("protocol", "https")
            host = url_obj.get("host", [])
            path = url_obj.get("path", [])
            base = f"{protocol}://{'.'.join(host)}" if host else ""
            if path:
                url = base + "/" + "/".join(path)
            else:
                url = base

    return url


def walk_items(items, parent_names=None, top_folder=None):
    """
    Recursively walk Postman 'item' array and yield (field_name, url, method, top_folder_name).
    top_folder_name is the first-level folder under collection root.
    """
    if parent_names is None:
        parent_names = []

    if not items:
        return

    for it in items:
        item_name = it.get("name", "Unnamed")
        children = it.get("item")
        request = it.get("request")

        # determine current top folder
        if parent_names:
            current_top = top_folder
        else:
            # this is a direct child of root collection
            current_top = item_name if children else item_name if top_folder is None else top_folder

        if children:
            # Folder
            new_parent = parent_names + [item_name]
            # if this is the first folder level, set top_folder to its name
            new_top = current_top if parent_names else item_name
            yield from walk_items(children, new_parent, new_top)
        elif request:
            url = extract_url(request)
            method = request.get("method", "GET")
            field_name = camel_case(*parent_names, item_name)
            yield field_name, url, method, (top_folder or current_top or "General")
