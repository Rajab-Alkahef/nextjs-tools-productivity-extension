"""
Routes generation snippets extractor
"""


def extract_routes_snippets(extractor):
    """Extract routes generation snippets in VS Code format"""
    routes_snippet = {
        "name": "Route Constants",
        "prefix": "next-routes",
        "body": [
            "// Routes for ${1:FeatureName}",
            "export abstract class ${1:FeatureName}Routes {",
            "\t// Add your routes here",
            "\tpublic static ${2:routeName} = \"/${3:route-path}\";",
            "}"
        ],
        "description": "Generates abstract class for route constants"
    }
    extractor._add_vscode_snippet("Routes", routes_snippet)
