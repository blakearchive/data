#!/usr/bin/env python3
"""
Data Validation Script for Blake Archive Data Repository

This script validates the integrity of the data files to ensure they're
compatible with the blakearchive/archive application.

Usage:
    python validate_data.py
"""

import csv
import glob
import os
import sys
from pathlib import Path

# Try to import lxml, fall back to built-in xml.etree
try:
    from lxml import etree
    XML_PARSER = 'lxml'
except ImportError:
    import xml.etree.ElementTree as etree
    XML_PARSER = 'xml.etree'

# ANSI color codes for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


class DataValidator:
    def __init__(self, data_dir='.'):
        self.data_dir = Path(data_dir)
        self.errors = []
        self.warnings = []
        self.successes = []

    def log_error(self, message):
        self.errors.append(message)
        print(f"{RED}✗ ERROR: {message}{RESET}")

    def log_warning(self, message):
        self.warnings.append(message)
        print(f"{YELLOW}⚠ WARNING: {message}{RESET}")

    def log_success(self, message):
        self.successes.append(message)
        print(f"{GREEN}✓ {message}{RESET}")

    def validate_directory_structure(self):
        """Validate that all required directories exist."""
        print("\n=== Validating Directory Structure ===")
        required_dirs = ['csv', 'works', 'info', 'exhibits', 'groups', 'previews', 'thesaurus']

        for dir_name in required_dirs:
            dir_path = self.data_dir / dir_name
            if dir_path.exists() and dir_path.is_dir():
                self.log_success(f"Directory '{dir_name}/' exists")
            else:
                self.log_error(f"Required directory '{dir_name}/' not found")

    def validate_csv_files(self):
        """Validate that all required CSV files exist and are readable."""
        print("\n=== Validating CSV Files ===")
        required_csvs = [
            'blake-relations.csv',
            'blake_superfast_matches.csv',
            'works.csv',
            'copy-handprints.csv',
            'home-page-images.csv'
        ]

        for csv_file in required_csvs:
            csv_path = self.data_dir / 'csv' / csv_file
            if not csv_path.exists():
                self.log_error(f"Required CSV file '{csv_file}' not found")
                continue

            try:
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    rows = list(reader)
                    if len(rows) > 0:
                        self.log_success(f"{csv_file}: {len(rows)-1} data rows (excluding header)")
                    else:
                        self.log_warning(f"{csv_file} is empty")
            except UnicodeDecodeError:
                self.log_error(f"{csv_file} is not UTF-8 encoded")
            except Exception as e:
                self.log_error(f"Error reading {csv_file}: {str(e)}")

    def validate_xml_files(self):
        """Validate XML files are well-formed."""
        print("\n=== Validating XML Files ===")
        xml_patterns = [
            ('works', 'works/*.xml'),
            ('info', 'info/*.xml'),
            ('groups', 'groups/*.xml'),
            ('thesaurus', 'thesaurus/*.xml')
        ]

        for category, pattern in xml_patterns:
            print(f"\nChecking {category}:")
            xml_files = list(self.data_dir.glob(pattern))

            if not xml_files:
                self.log_warning(f"No XML files found matching pattern '{pattern}'")
                continue

            valid_count = 0
            for xml_file in xml_files:
                try:
                    etree.parse(str(xml_file))
                    valid_count += 1
                except Exception as e:
                    error_type = type(e).__name__
                    if 'XMLSyntax' in error_type or 'ParseError' in error_type:
                        self.log_error(f"{xml_file.name}: XML syntax error - {str(e)}")
                    else:
                        self.log_error(f"{xml_file.name}: {str(e)}")

            if valid_count == len(xml_files):
                self.log_success(f"All {valid_count} {category} XML files are well-formed")
            else:
                self.log_warning(f"{valid_count}/{len(xml_files)} {category} XML files are valid")

    def validate_works_csv_references(self):
        """Validate that files referenced in works.csv exist."""
        print("\n=== Validating works.csv References ===")
        works_csv = self.data_dir / 'csv' / 'works.csv'

        if not works_csv.exists():
            return

        try:
            with open(works_csv, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)

            missing_info_files = []
            for row in rows:
                if 'info_filename' in row and row['info_filename']:
                    info_file = self.data_dir / 'info' / row['info_filename']
                    if not info_file.exists():
                        missing_info_files.append(row['info_filename'])

            if missing_info_files:
                self.log_warning(f"{len(missing_info_files)} info files referenced in works.csv not found")
                for filename in missing_info_files[:5]:  # Show first 5
                    print(f"  - {filename}")
                if len(missing_info_files) > 5:
                    print(f"  ... and {len(missing_info_files) - 5} more")
            else:
                self.log_success("All info files referenced in works.csv exist")

        except Exception as e:
            self.log_error(f"Error validating works.csv references: {str(e)}")

    def validate_exhibits(self):
        """Validate exhibit XML files."""
        print("\n=== Validating Exhibits ===")
        exhibit_files = list(self.data_dir.glob('exhibits/**/*.xml'))

        if not exhibit_files:
            self.log_warning("No exhibit files found")
            return

        valid_count = 0
        for exhibit_file in exhibit_files:
            try:
                tree = etree.parse(str(exhibit_file))
                # Basic validation: check if root element exists
                root = tree.getroot()
                if root is not None:
                    valid_count += 1
            except Exception as e:
                self.log_error(f"{exhibit_file.name}: {str(e)}")

        if valid_count == len(exhibit_files):
            self.log_success(f"All {valid_count} exhibit files are valid")
        else:
            self.log_warning(f"{valid_count}/{len(exhibit_files)} exhibit files are valid")

    def print_summary(self):
        """Print validation summary."""
        print("\n" + "="*60)
        print("VALIDATION SUMMARY")
        print("="*60)
        print(f"{GREEN}Successes: {len(self.successes)}{RESET}")
        print(f"{YELLOW}Warnings:  {len(self.warnings)}{RESET}")
        print(f"{RED}Errors:    {len(self.errors)}{RESET}")
        print("="*60)

        if self.errors:
            print(f"\n{RED}Validation failed with {len(self.errors)} error(s){RESET}")
            print("Please fix the errors above before importing data.")
            return False
        elif self.warnings:
            print(f"\n{YELLOW}Validation passed with {len(self.warnings)} warning(s){RESET}")
            print("The data can be imported, but you may want to review the warnings.")
            return True
        else:
            print(f"\n{GREEN}All validations passed!{RESET}")
            print("The data is ready to be imported.")
            return True

    def run_all_validations(self):
        """Run all validation checks."""
        print("Blake Archive Data Validation")
        print(f"Data directory: {self.data_dir.absolute()}")
        print(f"XML Parser: {XML_PARSER}")

        self.validate_directory_structure()
        self.validate_csv_files()
        self.validate_xml_files()
        self.validate_works_csv_references()
        self.validate_exhibits()

        success = self.print_summary()
        return 0 if success else 1


def main():
    """Main entry point."""
    data_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

    validator = DataValidator(data_dir)
    exit_code = validator.run_all_validations()

    sys.exit(exit_code)


if __name__ == '__main__':
    main()
