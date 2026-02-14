from pathlib import Path
from typing import Dict, Set, List
import sys
import os

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_json_file, get_all_keys


class UnusedKeysFinder:
    """Find translation keys in files but not used in code"""
    
    def __init__(self, translation_dir: Path, locale: str = 'en'):
        self.translation_dir = translation_dir
        self.locale = locale
        self.translation_file = translation_dir / f"{locale}.json"
    
    def find_unused_keys(self, extracted_keys: Set[str], namespace: str = None) -> Dict[str, any]:
        """Find keys that are in translation files but not used in code"""
        # Load existing translation file
        existing_translations = load_json_file(self.translation_file)
        existing_keys = get_all_keys(existing_translations)
        
        # Filter extracted keys by namespace if provided
        if namespace:
            # Keys might be prefixed with namespace or not
            namespace_extracted = set()
            for key in extracted_keys:
                if key.startswith(f"{namespace}."):
                    # Remove namespace prefix for comparison
                    namespace_extracted.add(key[len(namespace) + 1:])
                elif '.' not in key or key.split('.')[0] == namespace:
                    namespace_extracted.add(key)
            extracted_keys = namespace_extracted
        
        # Find unused keys
        unused_keys = existing_keys - extracted_keys
        
        unused_details = []
        for key in unused_keys:
            unused_details.append({
                'key': key,
                'namespace': namespace,
                'value': self._get_key_value(existing_translations, key)
            })
        
        return {
            'unused_keys': unused_keys,
            'unused_count': len(unused_keys),
            'total_in_file': len(existing_keys),
            'total_used': len(extracted_keys),
            'unused_details': unused_details
        }
    
    def _get_key_value(self, translations: dict, key_path: str) -> str:
        """Get the value of a key from nested dict"""
        keys = key_path.split('.')
        current = translations
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return ""
        return str(current) if not isinstance(current, dict) else "[nested object]"
    
    def find_unused_for_all_namespaces(self, namespace_keys: Dict[str, Set[str]]) -> Dict[str, Dict]:
        """Find unused keys for all namespaces"""
        results = {}
        
        for namespace, keys in namespace_keys.items():
            results[namespace] = self.find_unused_keys(keys, namespace)
        
        # Also check default/root namespace
        all_keys = set()
        for keys in namespace_keys.values():
            all_keys.update(keys)
        
        results['default'] = self.find_unused_keys(all_keys)
        
        return results
    
    def check_multiple_locales(self, extracted_keys: Set[str], locales: List[str]) -> Dict[str, Dict]:
        """Check unused keys across multiple locales"""
        results = {}
        
        for locale in locales:
            finder = UnusedKeysFinder(self.translation_dir, locale)
            results[locale] = finder.find_unused_keys(extracted_keys)
        
        return results
