import glob
import os
import pytest
from pathlib import Path

# These will be imported from the schemas repository
from schemas.python.json_formatter import format_file
from schemas.python.signals_testing import find_test_yaml_files, register_test_classes

REPO_ROOT = Path(__file__).parent.parent.absolute()
TEST_CASES_DIR = os.path.join(Path(__file__).parent, 'test_cases')

# Find all test files grouped by model year
test_files_by_year = find_test_yaml_files(TEST_CASES_DIR)

# Register test classes dynamically
register_test_classes(test_files_by_year)

def get_json_files():
    """Get all JSON files from the signalsets/v3 directory."""
    signalsets_path = os.path.join(REPO_ROOT, 'signalsets', 'v3')
    json_files = glob.glob(os.path.join(signalsets_path, '*.json'))
    # Convert full paths to relative filenames
    return [os.path.basename(f) for f in json_files]

@pytest.mark.parametrize("test_file",
    get_json_files(),
    ids=lambda x: x.split('.')[0].replace('-', '_')  # Create readable test IDs
)
def test_formatting(test_file):
    """Test signal set formatting for all vehicle models in signalsets/v3/."""
    signalset_path = os.path.join(REPO_ROOT, 'signalsets', 'v3', test_file)

    formatted = format_file(signalset_path)

    with open(signalset_path) as f:
        assert f.read() == formatted

if __name__ == '__main__':
    # Use pytest's main function with xdist arguments
    pytest.main([__file__, '-xvs', '-n', 'auto'])
