"""
Page generation snippets extractor
"""


def extract_page_snippets(extractor):
    """Extract page generation snippets in VS Code format"""
    page_snippet = {
        "name": "Page Template",
        "prefix": "next-page",
        "body": [
            "import ${1:ComponentName}Container from \"${2:./components}/${1:ComponentName}Container\";",
            "export default function ${1:ComponentName}Page() {",
            "\treturn <${1:ComponentName}Container />;",
            "}"
        ],
        "description": "Generates page.tsx file with dynamic route support"
    }
    extractor._add_vscode_snippet("Page Generation", page_snippet)
