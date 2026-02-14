"""
Types generation snippets extractor
"""


def extract_types_snippets(extractor):
    """Extract types generation snippets in VS Code format"""
    types_snippet = {
        "name": "Interface Definition",
        "prefix": "next-interface",
        "body": [
            "export interface ${1:InterfaceName} {",
            "\t${2:// Add your interface properties here}",
            "}"
        ],
        "description": "Generates TypeScript interface for the feature"
    }
    extractor._add_vscode_snippet("Types", types_snippet)
