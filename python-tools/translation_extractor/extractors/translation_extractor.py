import re
from pathlib import Path
from typing import List, Dict, Set, Optional
import sys
import os

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TranslationKeyExtractor:
    """Extract translation keys from code files"""
    
    def __init__(self):
        self.namespace_contexts = {}  # Track namespace per file/scope
    
    def extract_from_file(self, file_path: Path) -> Dict[str, any]:
        """Extract all translation keys from a file"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except Exception:
            return {
                'keys': set(),
                'namespaces': set(),
                'key_details': []
            }
        
        keys = set()
        namespaces = set()
        key_details = []
        
        # Extract namespace from useTranslations calls
        namespace_pattern = r'useTranslations\s*\(\s*["\']([^"\']+)["\']\s*\)'
        namespace_matches = re.finditer(namespace_pattern, content)
        for match in namespace_matches:
            namespace = match.group(1)
            namespaces.add(namespace)
            # Store namespace context (simplified - assumes one namespace per file)
            line_num = content[:match.start()].count('\n') + 1
            self.namespace_contexts[line_num] = namespace
        
        # Extract t() calls with simple keys
        # Pattern: t("key") or t('key')
        simple_key_pattern = r'\bt\s*\(\s*["\']([^"\']+)["\']\s*\)'
        simple_matches = re.finditer(simple_key_pattern, content)
        for match in simple_matches:
            key = match.group(1)
            keys.add(key)
            line_num = content[:match.start()].count('\n') + 1
            key_details.append({
                'key': key,
                'line': line_num,
                'type': 'simple',
                'namespace': self._get_namespace_for_line(line_num, namespaces)
            })
        
        # Extract t() calls with nested keys (namespace.key or form.name)
        nested_key_pattern = r'\bt\s*\(\s*["\']([^"\']+\.[^"\']+)["\']\s*\)'
        nested_matches = re.finditer(nested_key_pattern, content)
        for match in nested_matches:
            full_key = match.group(1)
            keys.add(full_key)
            line_num = content[:match.start()].count('\n') + 1
            # Extract namespace if present
            if '.' in full_key:
                parts = full_key.split('.')
                if len(parts) >= 2:
                    possible_namespace = parts[0]
                    if possible_namespace in namespaces:
                        key_details.append({
                            'key': full_key,
                            'line': line_num,
                            'type': 'nested',
                            'namespace': possible_namespace
                        })
                    else:
                        key_details.append({
                            'key': full_key,
                            'line': line_num,
                            'type': 'nested',
                            'namespace': None
                        })
        
        # Extract dynamic keys (t(keyVariable) - we'll note these but can't extract the actual key)
        dynamic_pattern = r'\bt\s*\(\s*([a-zA-Z_$][a-zA-Z0-9_$]*)\s*\)'
        dynamic_matches = re.finditer(dynamic_pattern, content)
        for match in dynamic_matches:
            var_name = match.group(1)
            # Skip if it's a known translation function parameter
            if var_name not in ('key', 'message', 'text'):
                line_num = content[:match.start()].count('\n') + 1
                key_details.append({
                    'key': f'[DYNAMIC:{var_name}]',
                    'line': line_num,
                    'type': 'dynamic',
                    'namespace': self._get_namespace_for_line(line_num, namespaces)
                })
        
        return {
            'keys': keys,
            'namespaces': namespaces,
            'key_details': key_details
        }
    
    def _get_namespace_for_line(self, line_num: int, namespaces: Set[str]) -> Optional[str]:
        """Get namespace context for a given line number"""
        # Simple heuristic: use the first namespace found before this line
        # In a real implementation, you'd track scope better
        if namespaces:
            return list(namespaces)[0]  # Return first namespace found
        return None
    
    def extract_from_directory(self, directory: Path, extensions: tuple = ('.ts', '.tsx', '.js', '.jsx')) -> Dict[str, any]:
        """Extract translation keys from all files in directory"""
        from utils import get_code_files
        
        all_keys = set()
        all_namespaces = set()
        file_results = {}
        
        files = get_code_files(directory, extensions)
        
        for file_path in files:
            result = self.extract_from_file(file_path)
            if result['keys'] or result['namespaces']:
                file_results[str(file_path.relative_to(directory))] = result
                all_keys.update(result['keys'])
                all_namespaces.update(result['namespaces'])
        
        return {
            'all_keys': all_keys,
            'all_namespaces': all_namespaces,
            'file_results': file_results
        }
    
    def get_keys_by_namespace(self, extraction_result: Dict) -> Dict[str, Set[str]]:
        """Group keys by namespace"""
        namespace_keys = {}
        
        for file_result in extraction_result.get('file_results', {}).values():
            for detail in file_result.get('key_details', []):
                namespace = detail.get('namespace') or 'default'
                key = detail.get('key')
                if key and not key.startswith('[DYNAMIC:'):
                    if namespace not in namespace_keys:
                        namespace_keys[namespace] = set()
                    namespace_keys[namespace].add(key)
        
        return namespace_keys
