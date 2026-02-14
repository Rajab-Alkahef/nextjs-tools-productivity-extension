"""
Functions for generating TypeScript code from parsed endpoints.
"""
from utils import camel_case, split_base_and_path, remove_postman_variables


def generate_ts_classes(endpoints, selected_folders):
    """
    Generate TypeScript class strings from a list of (field_name, url, method, folder).
    Creates a separate class for each selected folder. No base URL is used.
    """
    if not endpoints:
        return ""

    # Group by folder
    # endpoints: (field_name, url, method, folder)
    grouped = {}
    for field_name, url, method, folder in endpoints:
        if folder in selected_folders:
            grouped.setdefault(folder, []).append((field_name, url, method))

    if not grouped:
        return ""

    # Build TS - one class per folder
    all_lines = []

    # Sort folders for stable output
    for folder in sorted(grouped.keys()):
        class_name = camel_case(folder) + "EndPoints"
        lines = []
        lines.append(f"export abstract class {class_name} {{")
        lines.append("")

        for field_name, url, method in grouped[folder]:
            if not url:
                continue

            # Remove Postman variables like {{trustserviceURL}}
            url = remove_postman_variables(url)

            _, path = split_base_and_path(url)
            if not path.startswith("/"):
                path = "/" + path

            # Just use the path directly, no base URL
            lines.append(f'  public static {field_name} = `{path}`;')

        lines.append("")
        lines.append("}")
        all_lines.append("\n".join(lines))

    return "\n\n".join(all_lines)
