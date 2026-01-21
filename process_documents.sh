#!/bin/bash
# Quick script to process documents with attribution

# Default attribution text
ATTRIBUTION="Dr. Tara Salman"

# Check if input directory provided
if [ -z "$1" ]; then
    echo "Usage: $0 <input_directory> [output_directory]"
    echo "Example: $0 ~/Documents/attribution_needed/"
    exit 1
fi

INPUT_DIR="$1"
OUTPUT_DIR="${2:-${INPUT_DIR}/attributed}"

# Check if Python script exists
if [ ! -f "add_attribution.py" ]; then
    echo "Error: add_attribution.py not found in current directory"
    exit 1
fi

# Install dependencies if needed
echo "Checking dependencies..."
python3 -c "import PIL" 2>/dev/null || {
    echo "Installing dependencies..."
    uv pip install -r requirements_attribution.txt
}

# Process files
echo "Processing files in: $INPUT_DIR"
python3 add_attribution.py "$INPUT_DIR" -o "$OUTPUT_DIR" -t "$ATTRIBUTION"

echo "Done! Check output in: $OUTPUT_DIR"
