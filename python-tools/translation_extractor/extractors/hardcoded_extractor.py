from utils import suggest_translation_key
import re
from pathlib import Path
from typing import List, Dict, Tuple
import sys
import os

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class HardcodedStringExtractor:
    """Extract hardcoded strings from TypeScript/JavaScript files"""

    # Patterns to exclude (false positives)
    EXCLUDE_PATTERNS = [
        r'import\s+.*?from\s+["\']',  # Import statements
        r'require\s*\(["\']',  # Require statements
        r'console\.(log|error|warn|info|debug)\s*\(',  # Console statements
        r'["\']use\s+(client|server)["\']',  # React directives
        r'["\']use\s+strict["\']',  # Strict mode
        r'@ts-',  # TypeScript directives
        r'\/\/.*',  # Comments
        r'\/\*.*?\*\/',  # Block comments
        r'className\s*=\s*["\']',  # CSS classes (often intentional)
        r'id\s*=\s*["\']',  # IDs (often intentional)
        r'data-testid\s*=\s*["\']',  # Test IDs
        r'key\s*=\s*["\']',  # React keys
        r'href\s*=\s*["\']',  # URLs
        r'src\s*=\s*["\']',  # Source URLs
        r'type\s*[:=]\s*["\']',  # Type annotations
        r'as\s+["\']',  # Type assertions
        r'useTranslations\s*\(\s*["\']',  # Translation namespaces
        r'useState\s*\(',  # React useState
        r'useEffect\s*\(',  # React useEffect
        r'useCallback\s*\(',  # React useCallback
        r'useMemo\s*\(',  # React useMemo
        r'const\s+\w+\s*=\s*["\']',  # Variable assignments (often code)
        r'let\s+\w+\s*=\s*["\']',  # Let assignments
        r'var\s+\w+\s*=\s*["\']',  # Var assignments
    ]

    def __init__(self):
        self.exclude_regex = re.compile(
            '|'.join(self.EXCLUDE_PATTERNS), re.MULTILINE | re.DOTALL)

    def extract_from_file(self, file_path: Path) -> List[Dict[str, any]]:
        """Extract hardcoded strings from a single file"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return []

        results = []

        # Extract strings from JSX text content
        jsx_text_pattern = r'>\s*([^<>{}\n]+?)\s*<'
        jsx_matches = re.finditer(jsx_text_pattern, content)
        for match in jsx_matches:
            text = match.group(1).strip()
            if self._is_valid_string(text):
                results.append({
                    'text': text,
                    'line': content[:match.start()].count('\n') + 1,
                    'column': match.start() - content.rfind('\n', 0, match.start()) - 1,
                    'type': 'jsx_text',
                    'suggested_key': suggest_translation_key(text)
                })

        # Extract strings from JSX attributes (placeholder, title, aria-label, etc.)
        jsx_attr_pattern = r'(placeholder|title|aria-label|alt|label)\s*=\s*["\']([^"\']+)["\']'
        attr_matches = re.finditer(jsx_attr_pattern, content, re.IGNORECASE)
        for match in attr_matches:
            text = match.group(2).strip()
            if self._is_valid_string(text):
                results.append({
                    'text': text,
                    'line': content[:match.start()].count('\n') + 1,
                    'column': match.start() - content.rfind('\n', 0, match.start()) - 1,
                    'type': f'jsx_attr_{match.group(1).lower()}',
                    'suggested_key': suggest_translation_key(text)
                })

        # Extract string literals in code (but exclude common patterns)
        # More precise pattern: only match strings that are likely user-facing
        # Exclude strings in function calls, variable assignments, etc.
        string_literal_pattern = r'["\']([^"\']{3,})["\']'
        string_matches = re.finditer(string_literal_pattern, content)
        for match in string_matches:
            # Check if this match is in an excluded pattern
            match_start = match.start()
            match_end = match.end()

            # Get line context to check for comments and code context
            line_start = content.rfind('\n', 0, match_start) + 1
            line_end = content.find('\n', match_end)
            if line_end == -1:
                line_end = len(content)
            line_content = content[line_start:line_end]

            # Check if line contains comment markers before the string
            if '//' in line_content:
                comment_pos = line_content.find('//')
                if comment_pos < match_start - line_start:
                    continue  # Skip if comment is before the string

            # Get broader context to check for code patterns
            context_start = max(0, match_start - 150)
            context_end = min(len(content), match_end + 150)
            context = content[context_start:context_end]

            # Check if this is in an excluded pattern
            if self.exclude_regex.search(context):
                continue

            # Additional checks for code context
            # Skip if it's in a function call that's clearly code
            before_string = content[max(0, match_start - 50):match_start]
            after_string = content[match_end:min(len(content), match_end + 50)]

            # Skip if it looks like a translation namespace
            if re.search(r'useTranslations\s*\(\s*["\']', before_string):
                continue

            # Skip if it's in a useState, useEffect, etc.
            if re.search(r'(useState|useEffect|useCallback|useMemo|useRef)\s*\(', before_string):
                continue

            # Skip if it's clearly a variable assignment
            if re.search(r'(const|let|var)\s+\w+\s*=\s*["\']', before_string):
                continue

            # Skip if it's in JSX attribute that's not user-facing (like className, id, etc.)
            if re.search(r'(className|id|data-testid|key|href|src|type|as)\s*=\s*["\']', before_string, re.IGNORECASE):
                continue

            # Skip if it's part of a ternary or logical expression that's code
            if re.search(r'[?:]\s*["\']', before_string) and not re.search(r't\s*\(', before_string):
                continue

            text = match.group(1).strip()
            if self._is_valid_string(text):
                results.append({
                    'text': text,
                    'line': content[:match_start].count('\n') + 1,
                    'column': match_start - content.rfind('\n', 0, match_start) - 1,
                    'type': 'string_literal',
                    'suggested_key': suggest_translation_key(text)
                })

        # Extract template literals (but exclude common patterns)
        template_pattern = r'`([^`]{3,})`'
        template_matches = re.finditer(template_pattern, content)
        for match in template_matches:
            match_start = match.start()

            # Get line context to check for comments
            line_start = content.rfind('\n', 0, match_start) + 1
            line_end = content.find('\n', match_start)
            if line_end == -1:
                line_end = len(content)
            line_content = content[line_start:line_end]

            # Check if line contains comment markers before the template
            if '//' in line_content:
                comment_pos = line_content.find('//')
                if comment_pos < match_start - line_start:
                    continue  # Skip if comment is before the template

            context_start = max(0, match_start - 100)
            context_end = min(len(content), match_start + 200)
            context = content[context_start:context_end]

            if not self.exclude_regex.search(context):
                text = match.group(1).strip()
                # Skip if contains ${} (dynamic content)
                if '${' not in text and self._is_valid_string(text):
                    results.append({
                        'text': text,
                        'line': content[:match_start].count('\n') + 1,
                        'column': match_start - content.rfind('\n', 0, match_start) - 1,
                        'type': 'template_literal',
                        'suggested_key': suggest_translation_key(text)
                    })

        # Remove duplicates (same text, same line)
        seen = set()
        unique_results = []
        for result in results:
            key = (result['text'], result['line'])
            if key not in seen:
                seen.add(key)
                unique_results.append(result)

        return unique_results

    def _is_valid_string(self, text: str) -> bool:
        """Check if string is valid for translation"""
        if not text or len(text.strip()) < 2:
            return False

        # Exclude single characters, numbers, URLs, file paths
        if len(text.strip()) < 2:
            return False

        # Exclude URLs
        if text.startswith(('http://', 'https://', 'www.', 'mailto:')):
            return False

        # Exclude file paths
        if '/' in text and (text.startswith('/') or '\\' in text):
            return False

        # Exclude pure numbers
        if text.strip().replace('.', '').replace(',', '').isdigit():
            return False

        # Exclude CSS values
        if text.startswith(('#', 'rgb', 'rgba', 'var(')):
            return False

        # Exclude Tailwind classes (contain common Tailwind patterns)
        tailwind_patterns = [
            'flex', 'grid', 'gap-', 'space-', 'p-', 'px-', 'py-', 'pt-', 'pb-', 'pl-', 'pr-',
            'm-', 'mx-', 'my-', 'mt-', 'mb-', 'ml-', 'mr-', 'w-', 'h-', 'min-h-', 'max-w-',
            'bg-', 'text-', 'border-', 'rounded-', 'shadow-', 'hover:', 'focus:', 'sm:', 'md:', 'lg:',
            'items-', 'justify-', 'self-', 'col-', 'row-', 'resize-', 'min-h-', 'max-h-'
        ]
        text_lower = text.lower()
        if any(pattern in text_lower for pattern in tailwind_patterns):
            return False

        # Exclude code-like strings (contain operators, brackets, etc.)
        if re.search(r'[{}()\[\];=<>]', text):
            return False

        # Exclude strings that look like code (contain common code patterns)
        code_patterns = [
            'const ', 'let ', 'var ', 'function', '=>', '()', '{}', '[]',
            'useState', 'useEffect', 'onClick', 'onChange', 'setState',
            'className', 'value={', 'onChange=', 'e.target', 'e =>'
        ]
        if any(pattern in text for pattern in code_patterns):
            return False

        # Exclude strings that are mostly symbols or operators
        if len(re.sub(r'[a-zA-Z0-9\s]', '', text)) > len(text) * 0.5:
            return False

        # Must contain at least one letter
        if not re.search(r'[a-zA-Z]', text):
            return False

        # Exclude very short strings that are likely code identifiers
        if len(text.strip()) <= 3 and not re.search(r'[aeiouAEIOU]', text):
            return False

        return True

    def extract_from_directory(self, directory: Path, extensions: tuple = ('.ts', '.tsx', '.js', '.jsx')) -> Dict[str, List[Dict]]:
        """Extract hardcoded strings from all files in directory"""
        from utils import get_code_files

        results = {}
        files = get_code_files(directory, extensions)

        for file_path in files:
            file_results = self.extract_from_file(file_path)
            if file_results:
                results[str(file_path.relative_to(directory))] = file_results

        return results
