#!/usr/bin/env python3
"""
Tool for updating YAML test cases with current signal values.
This is useful when signals are removed from signalsets and tests need to be updated.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Add the current directory to the path so we can import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def ensure_schemas_repo():
    """Ensure the schemas repository is cloned, similar to devcontainer.json."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    schemas_dir = os.path.join(script_dir, 'schemas')

    # Check if schemas directory exists and is a git repository
    if os.path.isdir(os.path.join(schemas_dir, '.git')):
        # Try to pull latest changes
        try:
            print(f"Updating schemas repository...")
            subprocess.run(['git', 'pull'], cwd=schemas_dir, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to update schemas repository: {e}")
            # Continue with existing repo
            return True
    elif os.path.exists(schemas_dir):
        # Directory exists but might not be a git repository
        print(f"Warning: schemas directory exists but might not be a git repository: {schemas_dir}")
        return True
    else:
        # Need to clone the repository
        try:
            print(f"Cloning schemas repository...")
            subprocess.run(
                ['git', 'clone', '--depth=1', 'https://github.com/OBDb/.schemas.git', schemas_dir],
                check=True
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: Failed to clone schemas repository: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Update YAML test expected values based on current signalsets')
    parser.add_argument('--test-cases-dir', default=None, help='Path to test_cases directory')
    parser.add_argument('--year', type=int, action='append', help='Specific model year(s) to update')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be changed without making changes')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed output')

    args = parser.parse_args()

    # Find test_cases directory
    if args.test_cases_dir:
        test_cases_dir = args.test_cases_dir
    else:
        # Try to find it relative to current script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        test_cases_dir = os.path.join(script_dir, 'test_cases')

    if not os.path.isdir(test_cases_dir):
        print(f"Test cases directory not found: {test_cases_dir}")
        print(f"Creating directory: {test_cases_dir}")
        os.makedirs(test_cases_dir)

    print(f"Using test cases directory: {test_cases_dir}")

    # Ensure we have the schemas repository
    if not ensure_schemas_repo():
        print("Error: Could not set up schemas repository.")
        sys.exit(1)

    # Import our module
    try:
        from schemas.python.yaml_test_updater import update_yaml_tests
        update_yaml_tests(test_cases_dir, args.year, args.dry_run, args.verbose)
    except ImportError as e:
        print(f"Error importing yaml_test_updater module: {e}")
        print("Make sure the schemas package is properly installed.")
        sys.exit(1)
    except Exception as e:
        print(f"Error updating YAML tests: {e}")
        sys.exit(1)

    print("Done!")

if __name__ == "__main__":
    main()
