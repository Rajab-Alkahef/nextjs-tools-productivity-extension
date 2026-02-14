from pathlib import Path
from typing import Dict, Set, List
import sys
import os

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_json_file, get_all_keys


class MissingKeysFinder:
    """Find translation keys used in code but missing from translation files"""
    
    def __init__(self, translation_dir: Path, locale: str = 'en'):
        self.translation_dir = translation_dir
        self.locale = locale
        self.translation_file = translation_dir / f"{locale}.json"
    
    def find_missing_keys(self, extracted_keys: Set[str], namespace: str = None) -> Dict[str, any]:
        """Find keys that are in code but not in translation files"""
        # Load existing translation file
        existing_translations = load_json_file(self.translation_file)
        existing_keys = get_all_keys(existing_translations)
        
        # Normalize existing keys - remove leading dots and create variations
        normalized_existing = set()
        for key in existing_keys:
            normalized_existing.add(key)
            # Add without leading namespace if it has one
            if '.' in key:
                parts = key.split('.')
                # Add just the last part (key name)
                normalized_existing.add(parts[-1])
                # Add all variations
                for i in range(1, len(parts)):
                    normalized_existing.add('.'.join(parts[i:]))
        
        # Filter keys by namespace if provided
        if namespace:
            filtered_keys = {k for k in extracted_keys if k.startswith(f"{namespace}.") or k == namespace}
            # Also check keys without namespace prefix if they're in the namespace context
            namespace_keys = {k.split('.', 1)[1] if '.' in k else k for k in filtered_keys}
        else:
            namespace_keys = extracted_keys
        
        # Find missing keys
        missing_keys = set()
        missing_details = []
        
        for key in namespace_keys:
            # Check if key exists (with or without namespace prefix)
            key_exists = False
            
            # First check: exact match in normalized keys or existing keys
            if key in normalized_existing or key in existing_keys:
                key_exists = True
            # Second check: key exists at root level of JSON
            elif key in existing_translations:
                key_exists = True
            else:
                # Third check: if it's a nested key, check if it exists in the JSON structure
                parts = key.split('.')
                if len(parts) > 1:
                    current = existing_translations
                    found = True
                    for part in parts:
                        if isinstance(current, dict) and part in current:
                            current = current[part]
                        else:
                            found = False
                            break
                    if found:
                        key_exists = True
                
                # Fourth check: check if the key name (last part) exists anywhere
                if not key_exists:
                    key_name = parts[-1] if parts else key
                    # Check if key name exists at root
                    if key_name in existing_translations:
                        key_exists = True
                    # Check if key name is the last part of any existing key
                    elif any(k.split('.')[-1] == key_name for k in existing_keys):
                        key_exists = True
            
            if not key_exists:
                missing_keys.add(key)
                missing_details.append({
                    'key': key,
                    'namespace': namespace,
                    'suggested_path': self._suggest_key_path(key, namespace)
                })
        
        return {
            'missing_keys': missing_keys,
            'missing_count': len(missing_keys),
            'existing_count': len(existing_keys),
            'total_extracted': len(namespace_keys),
            'missing_details': missing_details
        }
    
    def find_missing_for_all_namespaces(self, namespace_keys: Dict[str, Set[str]]) -> Dict[str, Dict]:
        """Find missing keys for all namespaces"""
        results = {}
        
        for namespace, keys in namespace_keys.items():
            results[namespace] = self.find_missing_keys(keys, namespace)
        
        # Also check default/root namespace
        all_keys = set()
        for keys in namespace_keys.values():
            all_keys.update(keys)
        
        results['default'] = self.find_missing_keys(all_keys)
        
        return results
    
    def _suggest_key_path(self, key: str, namespace: str = None) -> str:
        """Suggest the path structure for a key in JSON"""
        if namespace:
            return f"{namespace}.{key}"
        return key
    
    def check_multiple_locales(self, extracted_keys: Set[str], locales: List[str]) -> Dict[str, Dict]:
        """Check missing keys across multiple locales"""
        results = {}
        
        for locale in locales:
            finder = MissingKeysFinder(self.translation_dir, locale)
            results[locale] = finder.find_missing_keys(extracted_keys)
        
        return results
