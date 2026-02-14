"""
Components generation snippets extractor
"""


def extract_components_snippets(extractor):
    """Extract component generation snippets in VS Code format"""
    component_snippet = {
        "name": "Container Component",
        "prefix": "next-container",
        "body": [
            "import BasePage from \"@/components/BasePage\";",
            "",
            "export default function ${1:ComponentName}Container() {",
            "\treturn (",
            "\t\t<BasePage>",
            "\t\t\t<div className=\"flex flex-col bg-card rounded-xl space-y-4\">",
            "\t\t\t\t${2:// content}",
            "\t\t\t</div>",
            "\t\t</BasePage>",
            "\t);",
            "}"
        ],
        "description": "Generates a container component with BasePage wrapper"
    }
    extractor._add_vscode_snippet("Components", component_snippet)
