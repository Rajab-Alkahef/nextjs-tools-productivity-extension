#!/usr/bin/env python3
"""
CLI interface for Translation Key Extractor
"""
import argparse
import sys
import json
from pathlib import Path
from typing import List

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from extractors.hardcoded_extractor import HardcodedStringExtractor
from extractors.translation_extractor import TranslationKeyExtractor
from extractors.missing_keys_finder import MissingKeysFinder
from extractors.unused_keys_finder import UnusedKeysFinder
from generators.translation_generator import TranslationFileGenerator


def print_results(data: dict, format: str = 'text'):
    """Print results in specified format"""
    if format == 'json':
        print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        # Text format
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, (list, dict)):
                    print(f"\n{key}:")
                    print_results(value, format)
                else:
                    print(f"{key}: {value}")
        elif isinstance(data, list):
            for item in data:
                print(f"  - {item}")


def cmd_scan(args):
    """Scan directory for hardcoded strings"""
    extractor = HardcodedStringExtractor()
    source_dir = Path(args.source_dir)
    
    if not source_dir.exists():
        print(f"Error: Directory {source_dir} does not exist")
        return 1
    
    results = extractor.extract_from_directory(source_dir)
    
    total_strings = sum(len(strings) for strings in results.values())
    print(f"Found {total_strings} hardcoded strings in {len(results)} files")
    
    if args.output:
        output_file = Path(args.output)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {output_file}")
    else:
        print_results(results, args.format)
    
    return 0


def cmd_extract(args):
    """Extract translation keys from code"""
    extractor = TranslationKeyExtractor()
    source_dir = Path(args.source_dir)
    
    if not source_dir.exists():
        print(f"Error: Directory {source_dir} does not exist")
        return 1
    
    results = extractor.extract_from_directory(source_dir)
    
    print(f"Found {len(results['all_keys'])} unique translation keys")
    print(f"Found {len(results['all_namespaces'])} namespaces: {', '.join(results['all_namespaces'])}")
    
    if args.output:
        output_file = Path(args.output)
        # Convert sets to lists for JSON serialization
        output_data = {
            'all_keys': list(results['all_keys']),
            'all_namespaces': list(results['all_namespaces']),
            'file_results': {
                file: {
                    'keys': list(data['keys']),
                    'namespaces': list(data['namespaces']),
                    'key_details': data['key_details']
                }
                for file, data in results['file_results'].items()
            }
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"Results saved to {output_file}")
    else:
        print(f"\nKeys found:")
        for key in sorted(results['all_keys']):
            print(f"  - {key}")
    
    return 0


def cmd_find_missing(args):
    """Find missing translation keys"""
    translation_dir = Path(args.translations)
    locale = args.locale
    
    if not translation_dir.exists():
        print(f"Error: Translation directory {translation_dir} does not exist")
        return 1
    
    # First extract keys from code
    extractor = TranslationKeyExtractor()
    source_dir = Path(args.source_dir)
    extraction_results = extractor.extract_from_directory(source_dir)
    
    # Find missing keys
    finder = MissingKeysFinder(translation_dir, locale)
    results = finder.find_missing_keys(extraction_results['all_keys'])
    
    print(f"Missing keys for locale '{locale}': {results['missing_count']}")
    print(f"Existing keys: {results['existing_count']}")
    print(f"Total extracted keys: {results['total_extracted']}")
    
    if results['missing_keys']:
        print("\nMissing keys:")
        for detail in results['missing_details']:
            print(f"  - {detail['key']}")
    
    if args.output:
        output_file = Path(args.output)
        output_data = {
            'locale': locale,
            'missing_keys': list(results['missing_keys']),
            'missing_count': results['missing_count'],
            'existing_count': results['existing_count'],
            'total_extracted': results['total_extracted'],
            'missing_details': results['missing_details']
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {output_file}")
    
    return 0


def cmd_find_unused(args):
    """Find unused translation keys"""
    translation_dir = Path(args.translations)
    locale = args.locale
    
    if not translation_dir.exists():
        print(f"Error: Translation directory {translation_dir} does not exist")
        return 1
    
    # First extract keys from code
    extractor = TranslationKeyExtractor()
    source_dir = Path(args.source_dir)
    extraction_results = extractor.extract_from_directory(source_dir)
    
    # Find unused keys
    finder = UnusedKeysFinder(translation_dir, locale)
    results = finder.find_unused_keys(extraction_results['all_keys'])
    
    print(f"Unused keys for locale '{locale}': {results['unused_count']}")
    print(f"Total keys in file: {results['total_in_file']}")
    print(f"Keys used in code: {results['total_used']}")
    
    if results['unused_keys']:
        print("\nUnused keys:")
        for detail in results['unused_details'][:50]:  # Limit to first 50
            print(f"  - {detail['key']} (value: {detail['value'][:50]})")
        if len(results['unused_keys']) > 50:
            print(f"... and {len(results['unused_keys']) - 50} more")
    
    if args.output:
        output_file = Path(args.output)
        output_data = {
            'locale': locale,
            'unused_keys': list(results['unused_keys']),
            'unused_count': results['unused_count'],
            'total_in_file': results['total_in_file'],
            'total_used': results['total_used'],
            'unused_details': results['unused_details']
        }
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {output_file}")
    
    return 0


def cmd_update(args):
    """Update translation files with missing keys"""
    translation_dir = Path(args.translations)
    locale = args.locale
    
    if not translation_dir.exists():
        print(f"Error: Translation directory {translation_dir} does not exist")
        return 1
    
    # First extract keys and find missing
    extractor = TranslationKeyExtractor()
    source_dir = Path(args.source_dir)
    extraction_results = extractor.extract_from_directory(source_dir)
    
    finder = MissingKeysFinder(translation_dir, locale)
    missing_results = finder.find_missing_keys(extraction_results['all_keys'])
    
    if not missing_results['missing_keys']:
        print(f"No missing keys found for locale '{locale}'")
        return 0
    
    # Update translation file
    generator = TranslationFileGenerator(translation_dir, locale)
    update_results = generator.update_file(
        missing_results['missing_keys'],
        auto_fill=args.auto_fill
    )
    
    if update_results['success']:
        print(f"Successfully updated {update_results['added_count']} keys in {translation_dir / f'{locale}.json'}")
        if update_results['skipped_count'] > 0:
            print(f"Skipped {update_results['skipped_count']} keys (already exist)")
    else:
        print("Error: Failed to update translation file")
        return 1
    
    return 0


def main():
    parser = argparse.ArgumentParser(
        description='Translation Key Extractor - Manage translations in Next.js projects'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan for hardcoded strings')
    scan_parser.add_argument('source_dir', help='Source directory to scan')
    scan_parser.add_argument('--output', '-o', help='Output file path (JSON)')
    scan_parser.add_argument('--format', '-f', choices=['text', 'json'], default='text',
                           help='Output format')
    
    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract translation keys from code')
    extract_parser.add_argument('source_dir', help='Source directory to scan')
    extract_parser.add_argument('--output', '-o', help='Output file path (JSON)')
    extract_parser.add_argument('--format', '-f', choices=['text', 'json'], default='text',
                              help='Output format')
    
    # Find missing command
    missing_parser = subparsers.add_parser('find-missing', help='Find missing translation keys')
    missing_parser.add_argument('source_dir', help='Source directory to scan')
    missing_parser.add_argument('--translations', '-t', required=True,
                              help='Translation directory (e.g., messages/)')
    missing_parser.add_argument('--locale', '-l', default='en',
                               help='Locale to check (default: en)')
    missing_parser.add_argument('--output', '-o', help='Output file path (JSON)')
    
    # Find unused command
    unused_parser = subparsers.add_parser('find-unused', help='Find unused translation keys')
    unused_parser.add_argument('source_dir', help='Source directory to scan')
    unused_parser.add_argument('--translations', '-t', required=True,
                              help='Translation directory (e.g., messages/)')
    unused_parser.add_argument('--locale', '-l', default='en',
                              help='Locale to check (default: en)')
    unused_parser.add_argument('--output', '-o', help='Output file path (JSON)')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update translation files with missing keys')
    update_parser.add_argument('source_dir', help='Source directory to scan')
    update_parser.add_argument('--translations', '-t', required=True,
                              help='Translation directory (e.g., messages/)')
    update_parser.add_argument('--locale', '-l', default='en',
                              help='Locale to update (default: en)')
    update_parser.add_argument('--auto-fill', action='store_true',
                              help='Auto-fill missing keys with default values')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate command
    commands = {
        'scan': cmd_scan,
        'extract': cmd_extract,
        'find-missing': cmd_find_missing,
        'find-unused': cmd_find_unused,
        'update': cmd_update
    }
    
    command_func = commands.get(args.command)
    if command_func:
        return command_func(args)
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())
