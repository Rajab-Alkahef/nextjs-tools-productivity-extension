"""
Utility functions for snippet viewer
"""
import json
from typing import Dict


def format_vscode_snippet(snippet: Dict) -> str:
    """Format a snippet as VS Code JSON string"""
    vs_code_snippet = {
        snippet['name']: {
            "prefix": snippet['prefix'],
            "body": snippet['body'],
            "description": snippet['description']
        }
    }
    return json.dumps(vs_code_snippet, indent="\t", ensure_ascii=False)
