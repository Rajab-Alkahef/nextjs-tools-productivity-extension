"""
Hooks generation snippets extractor
"""


def extract_hooks_snippets(extractor):
    """Extract hooks generation snippets in VS Code format"""
    hook_snippet = {
        "name": "Custom Hook",
        "prefix": "next-hook",
        "body": [
            "export const use${1:HookName} = () => {",
            "\t${2:// Add your hook logic here}",
            "\treturn {};",
            "}"
        ],
        "description": "Generates a custom React hook"
    }
    extractor._add_vscode_snippet("Hooks", hook_snippet)
