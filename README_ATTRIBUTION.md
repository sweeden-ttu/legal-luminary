# Attribution Script

This script adds attribution text to images and PDF documents with rotation passes.

## Installation

Install required dependencies:

```bash
uv pip install -r requirements_attribution.txt
```

Note: `pdf2image` requires `poppler` to be installed on your system:
- **macOS**: `brew install poppler`
- **Linux**: `sudo apt-get install poppler-utils` (Debian/Ubuntu) or `sudo yum install poppler-utils` (RHEL/CentOS)
- **Windows**: Download from [poppler-windows](https://github.com/oschwartz10612/poppler-windows/releases)

## Usage

### Process a single image file:
```bash
python add_attribution.py probability2.jpg
```

### Process a single PDF file:
```bash
python add_attribution.py document.pdf
```

### Process all files in a directory:
```bash
python add_attribution.py /path/to/documents/
```

### Specify output location:
```bash
python add_attribution.py input.jpg -o output_base
python add_attribution.py /path/to/documents/ -o /path/to/output/
```

### Custom attribution text:
```bash
python add_attribution.py file.jpg -t "Dr. Tara Salman"
```

### Custom font size:
```bash
python add_attribution.py file.jpg -s 24
```

## Features

- **Two-pass rotation processing:**
  - **Pass 1**: Rotates image 90°, adds attribution, saves as `filename_pass1.ext`
  - **Pass 2**: Rotates additional 250° (340° total from original), adds attribution, saves as `filename_pass2.ext`
- **Dual-color attribution**: Adds both black and white text
  - Black text at base position (bottom-left)
  - White text offset by +2px on x-axis, +3px on y-axis
- **Dimension-aware positioning**: Calculates bottom-left corner based on current image dimensions after rotation
- Processes JPG, PNG, and PDF files
- Preserves image quality
- Handles multi-page PDFs
- Batch processing support

## Output

- Single files: Creates `filename_pass1.ext` and `filename_pass2.ext` in the same directory
- Directories: Creates an `attributed/` subdirectory with processed files (each with pass1 and pass2 versions)
