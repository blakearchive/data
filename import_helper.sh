#!/bin/bash
# Blake Archive Data Import Helper Script
#
# This script helps automate the data import process for the Blake Archive.
# It validates data, imports it into the database, and rebuilds search indexes.
#
# Usage:
#   ./import_helper.sh [options]
#
# Options:
#   --skip-validation    Skip data validation step
#   --skip-homepage      Skip homepage import
#   --skip-solr          Skip Solr reindexing
#   --archive-path PATH  Path to archive repository (default: ../archive)
#   --help               Show this help message

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
SKIP_VALIDATION=false
SKIP_HOMEPAGE=false
SKIP_SOLR=false
ARCHIVE_PATH="../archive"
DATA_PATH="$(pwd)"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-validation)
            SKIP_VALIDATION=true
            shift
            ;;
        --skip-homepage)
            SKIP_HOMEPAGE=true
            shift
            ;;
        --skip-solr)
            SKIP_SOLR=true
            shift
            ;;
        --archive-path)
            ARCHIVE_PATH="$2"
            shift 2
            ;;
        --help)
            echo "Blake Archive Data Import Helper"
            echo ""
            echo "Usage: ./import_helper.sh [options]"
            echo ""
            echo "Options:"
            echo "  --skip-validation    Skip data validation step"
            echo "  --skip-homepage      Skip homepage import"
            echo "  --skip-solr          Skip Solr reindexing"
            echo "  --archive-path PATH  Path to archive repository (default: ../archive)"
            echo "  --help               Show this help message"
            exit 0
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

# Function to print section headers
print_header() {
    echo ""
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================================${NC}"
}

# Function to print success messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

# Function to print error messages
print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Function to print warning messages
print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Function to print info messages
print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

# Check if we're in the data repository
if [ ! -f "validate_data.py" ]; then
    print_error "This script must be run from the Blake Archive data repository root"
    exit 1
fi

# Check if archive repository exists
if [ ! -d "$ARCHIVE_PATH" ]; then
    print_error "Archive repository not found at: $ARCHIVE_PATH"
    print_info "Use --archive-path to specify the correct path"
    exit 1
fi

# Check if import scripts exist
BLAKEARCHIVE_PATH="$ARCHIVE_PATH/blakearchive"
if [ ! -f "$BLAKEARCHIVE_PATH/import.py" ]; then
    print_error "import.py not found at: $BLAKEARCHIVE_PATH/import.py"
    exit 1
fi

print_header "Blake Archive Data Import"
echo "Data path: $DATA_PATH"
echo "Archive path: $ARCHIVE_PATH"
echo ""

# Step 1: Validate data
if [ "$SKIP_VALIDATION" = false ]; then
    print_header "Step 1: Validating Data"
    if python3 validate_data.py; then
        print_success "Data validation passed"
    else
        print_error "Data validation failed"
        print_info "Fix validation errors or use --skip-validation to skip this step"
        exit 1
    fi
else
    print_warning "Skipping data validation"
fi

# Step 2: Import main data
print_header "Step 2: Importing Main Data"
print_info "This may take several minutes..."
cd "$BLAKEARCHIVE_PATH"

if python3 import.py "$DATA_PATH"; then
    print_success "Main data import completed"
else
    print_error "Main data import failed"
    exit 1
fi

# Step 3: Import Solr indexes
if [ "$SKIP_SOLR" = false ]; then
    print_header "Step 3: Rebuilding Solr Indexes"
    print_info "This may take a few minutes..."

    # Check if Solr is running
    if curl -s "http://localhost:8983/solr/admin/cores?action=STATUS" > /dev/null 2>&1; then
        if python3 solrimport.py; then
            print_success "Solr indexes rebuilt"
        else
            print_error "Solr import failed"
            print_warning "Continuing anyway..."
        fi
    else
        print_warning "Solr doesn't appear to be running at localhost:8983"
        print_info "Skipping Solr import"
    fi
else
    print_warning "Skipping Solr reindexing"
fi

# Step 4: Import homepage data
if [ "$SKIP_HOMEPAGE" = false ]; then
    print_header "Step 4: Importing Homepage Data"

    if python3 homepageimport.py "$DATA_PATH"; then
        print_success "Homepage data import completed"
    else
        print_error "Homepage import failed"
        print_warning "Continuing anyway..."
    fi
else
    print_warning "Skipping homepage import"
fi

# Done
print_header "Import Complete"
print_success "All import steps completed successfully!"
echo ""
print_info "Next steps:"
echo "  1. Restart the Flask server if it's running"
echo "  2. Clear your browser cache"
echo "  3. Verify changes in the application"
echo ""

cd "$DATA_PATH"
