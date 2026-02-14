from pathlib import Path
from typing import Dict, Set, List, Optional
import sys
import os

# Add parent directory to path for utils import
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_json_file, save_json_file, set_nested_value, get_nested_value, suggest_translation_key


class TranslationFileGenerator:
    """Generate and update translation JSON files"""
    
    def __init__(self, translation_dir: Path, locale: str = 'en'):
        self.translation_dir = translation_dir
        self.locale = locale
        self.translation_file = translation_dir / f"{locale}.json"
    
    def generate_file(self, keys: Set[str], auto_fill: bool = False, 
                     default_value: str = None) -> bool:
        """Generate a new translation file with the given keys"""
        translations = load_json_file(self.translation_file)
        
        for key in keys:
            # Check if key already exists
            existing_value = get_nested_value(translations, key)
            if existing_value is None:
                # Add new key
                if auto_fill:
                    # Use the key itself or suggested translation
                    value = default_value or key.replace('.', ' ').title()
                else:
                    value = default_value or f"[TODO: Translate {key}]"
                set_nested_value(translations, key, value)
        
        return save_json_file(self.translation_file, translations)
    
    def update_file(self, missing_keys: Set[str], auto_fill: bool = False,
                   default_value: str = None) -> Dict[str, any]:
        """Update existing translation file with missing keys"""
        translations = load_json_file(self.translation_file)
        added_keys = []
        skipped_keys = []
        
        for key in missing_keys:
            # Check if key already exists
            existing_value = get_nested_value(translations, key)
            if existing_value is None:
                # Add new key
                if auto_fill:
                    value = default_value or key.replace('.', ' ').title()
                else:
                    value = default_value or f"[TODO: Translate {key}]"
                set_nested_value(translations, key, value)
                added_keys.append(key)
            else:
                skipped_keys.append(key)
        
        # Save updated file
        success = save_json_file(self.translation_file, translations)
        
        return {
            'success': success,
            'added_keys': added_keys,
            'skipped_keys': skipped_keys,
            'added_count': len(added_keys),
            'skipped_count': len(skipped_keys)
        }
    
    def update_multiple_locales(self, missing_keys: Set[str], locales: List[str],
                               auto_fill: bool = False) -> Dict[str, Dict]:
        """Update multiple locale files with missing keys"""
        results = {}
        
        for locale in locales:
            generator = TranslationFileGenerator(self.translation_dir, locale)
            results[locale] = generator.update_file(missing_keys, auto_fill)
        
        return results
    
    def organize_by_namespace(self, keys: Set[str], namespace: str) -> Dict[str, Set[str]]:
        """Organize keys by namespace structure"""
        namespace_keys = {}
        
        for key in keys:
            if key.startswith(f"{namespace}."):
                # Remove namespace prefix
                sub_key = key[len(namespace) + 1:]
                if namespace not in namespace_keys:
                    namespace_keys[namespace] = set()
                namespace_keys[namespace].add(sub_key)
            elif '.' not in key:
                # Root level key
                if 'default' not in namespace_keys:
                    namespace_keys['default'] = set()
                namespace_keys['default'].add(key)
        
        return namespace_keys
    
    def merge_translations(self, source_file: Path, target_file: Path,
                          overwrite: bool = False) -> bool:
        """Merge translations from source file to target file"""
        source_translations = load_json_file(source_file)
        target_translations = load_json_file(target_file)
        
        def merge_dict(source: dict, target: dict):
            for key, value in source.items():
                if key in target:
                    if isinstance(value, dict) and isinstance(target[key], dict):
                        merge_dict(value, target[key])
                    elif overwrite:
                        target[key] = value
                else:
                    target[key] = value
        
        merge_dict(source_translations, target_translations)
        return save_json_file(target_file, target_translations)
    
    def format_file(self) -> bool:
        """Format and save the translation file (pretty print)"""
        translations = load_json_file(self.translation_file)
        return save_json_file(self.translation_file, translations, indent=2)
