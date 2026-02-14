"""
Main snippet extractor class
"""
from typing import Dict, List
import json
import sys
import os

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import format_vscode_snippet

from .page_extractor import extract_page_snippets
from .components_extractor import extract_components_snippets
from .hooks_extractor import extract_hooks_snippets
from .config_extractor import extract_config_snippets
from .types_extractor import extract_types_snippets
from .services_extractor import extract_services_snippets
from .redux_extractor import extract_redux_snippets
from .routes_extractor import extract_routes_snippets


class SnippetExtractor:
    """Extracts code snippets from generate feature files and groups them by topic"""

    def __init__(self):
        self.snippets: Dict[str, List[Dict[str, str]]] = {
            "Page Generation": [],
            "Components": [],
            "Hooks": [],
            "Config": [],
            "Types": [],
            "Services": [],
            "Redux": [],
            "Routes": [],
            "TypeScript Snippets": [],
            "All": []
        }

    def _add_vscode_snippet(self, topic: str, snippet: Dict):
        """Add snippet in VS Code format to topic and All group"""
        # Format as JSON string for display
        formatted_json = format_vscode_snippet(snippet)

        # Create display snippet
        display_snippet = {
            "name": snippet['name'],
            "description": f"Prefix: '{snippet['prefix']}' - {snippet['description']}",
            "code": formatted_json,
            "topic": topic  # Store topic for "All" group organization
        }

        # Add to topic
        self.snippets[topic].append(display_snippet)

        # Add to "All" with topic prefix in name
        all_snippet = display_snippet.copy()
        all_snippet["name"] = f"[{topic}] {snippet['name']}"
        self.snippets["All"].append(all_snippet)

    def extract_all_snippets(self):
        """Extract all snippets from all topics"""
        extract_page_snippets(self)
        extract_components_snippets(self)
        extract_hooks_snippets(self)
        extract_config_snippets(self)
        extract_types_snippets(self)
        extract_services_snippets(self)
        extract_redux_snippets(self)
        extract_routes_snippets(self)
        
        # Extract TypeScript snippets
        from snippets.typescript_snippets import TYPESCRIPT_SNIPPETS
        for snippet in TYPESCRIPT_SNIPPETS:
            self._add_vscode_snippet("TypeScript Snippets", snippet)
