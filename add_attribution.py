#!/usr/bin/env python3
"""
Script to add attribution to images and PDF documents with rotation passes.
Pass 1: Rotate 90 degrees, add attribution
Pass 2: Rotate additional 250 degrees (340 total), make copy, add attribution
Each pass adds both black and white text with offset.
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import argparse
import math

try:
    from pdf2image import convert_from_path
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False
    print("Warning: pdf2image not installed. PDF support disabled.")
    print("Install with: uv pip install pdf2image")

try:
    from PyPDF2 import PdfWriter, PdfReader
    PDF_MERGE_SUPPORT = True
except ImportError:
    PDF_MERGE_SUPPORT = False
    print("Warning: PyPDF2 not installed. PDF merging disabled.")
    print("Install with: uv pip install PyPDF2")


def get_font(size=20):
    """Get a font, trying system fonts first, then default."""
    try:
        # Try to use a system font
        if sys.platform == "darwin":  # macOS
            font_path = "/System/Library/Fonts/Helvetica.ttc"
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        elif sys.platform.startswith("linux"):
            font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
        elif sys.platform == "win32":
            font_path = "C:/Windows/Fonts/arial.ttf"
            if os.path.exists(font_path):
                return ImageFont.truetype(font_path, size)
    except:
        pass
    
    # Fallback to default font
    try:
        return ImageFont.truetype("arial.ttf", size)
    except:
        return ImageFont.load_default()


def rotate_image(image, angle):
    """
    Rotate image by angle degrees, expanding canvas to fit.
    
    Args:
        image: PIL Image object
        angle: Rotation angle in degrees (positive = counterclockwise)
    
    Returns:
        Rotated PIL Image
    """
    # Expand=True ensures the entire rotated image is visible
    return image.rotate(angle, expand=True, fillcolor='white')


def get_bottom_left_position(width, height, text_width, text_height, padding=10):
    """
    Calculate bottom-left position for text based on image dimensions.
    
    Args:
        width: Image width
        height: Image height
        text_width: Text width
        text_height: Text height
        padding: Padding from edges
    
    Returns:
        (x, y) tuple for text position
    """
    x = padding
    y = height - text_height - padding
    return (x, y)


def add_attribution_to_image(image, attribution_text="Dr. Tara Salman", 
                            font_size=20, padding=10, x_offset=2, y_offset=3):
    """
    Add attribution text to an image in the bottom left corner.
    Adds both black and white text with specified offset.
    
    Args:
        image: PIL Image object
        attribution_text: Text to add
        font_size: Size of the font
        padding: Padding from edges
        x_offset: X-axis offset for white text (pixels)
        y_offset: Y-axis offset for white text (pixels)
    
    Returns:
        PIL Image with attribution added
    """
    # Create a copy to avoid modifying original
    img = image.copy()
    draw = ImageDraw.Draw(img)
    
    # Get image dimensions
    width, height = img.size
    print(f"    Image dimensions: {width} x {height}")
    
    # Get font
    font = get_font(font_size)
    
    # Get text dimensions
    bbox = draw.textbbox((0, 0), attribution_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate bottom-left position based on current image dimensions
    x, y = get_bottom_left_position(width, height, text_width, text_height, padding)
    
    # Draw black text first (base position)
    draw.text((x, y), attribution_text, font=font, fill="black")
    
    # Draw white text with offset
    draw.text((x + x_offset, y + y_offset), attribution_text, font=font, fill="white")
    
    return img


def process_image_with_passes(input_path, output_base_path=None, 
                              attribution_text="Dr. Tara Salman",
                              font_size=20):
    """
    Process an image file with two rotation passes.
    Pass 1: Rotate 90°, add attribution, save
    Pass 2: Rotate additional 250° (340° total), add attribution, save as copy
    
    Args:
        input_path: Path to input image
        output_base_path: Base path for output (if None, uses input path stem)
        attribution_text: Text to add
        font_size: Font size
    
    Returns:
        List of output file paths
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Image not found: {input_path}")
    
    if output_base_path is None:
        output_base_path = input_path.parent / input_path.stem
    else:
        output_base_path = Path(output_base_path)
    
    print(f"Processing image: {input_path.name}")
    
    # Open and prepare image
    image = Image.open(input_path)
    
    # Convert to RGB if necessary (for JPEG compatibility)
    if image.mode in ('RGBA', 'LA', 'P'):
        # Create white background for transparent images
        rgb_image = Image.new('RGB', image.size, (255, 255, 255))
        if image.mode == 'P':
            image = image.convert('RGBA')
        rgb_image.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
        image = rgb_image
    elif image.mode != 'RGB':
        image = image.convert('RGB')
    
    original_size = image.size
    print(f"  Original dimensions: {original_size[0]} x {original_size[1]}")
    
    output_files = []
    
    # PASS 1: Rotate 90 degrees
    print("  Pass 1: Rotating 90 degrees...")
    rotated_90 = rotate_image(image, 90)
    print(f"    After 90° rotation: {rotated_90.size[0]} x {rotated_90.size[1]}")
    
    # Add attribution
    attributed_90 = add_attribution_to_image(
        rotated_90, attribution_text, font_size=font_size
    )
    
    # Save pass 1
    output_path_1 = output_base_path.parent / f"{output_base_path.name}_pass1{input_path.suffix}"
    attributed_90.save(output_path_1, quality=95)
    print(f"  Pass 1 saved to: {output_path_1}")
    output_files.append(output_path_1)
    
    # PASS 2: Rotate additional 250 degrees (340 total from original)
    print("  Pass 2: Rotating additional 250 degrees (340° total)...")
    rotated_340 = rotate_image(rotated_90, 250)
    print(f"    After 340° rotation: {rotated_340.size[0]} x {rotated_340.size[1]}")
    
    # Add attribution
    attributed_340 = add_attribution_to_image(
        rotated_340, attribution_text, font_size=font_size
    )
    
    # Save pass 2 (copy)
    output_path_2 = output_base_path.parent / f"{output_base_path.name}_pass2{input_path.suffix}"
    attributed_340.save(output_path_2, quality=95)
    print(f"  Pass 2 saved to: {output_path_2}")
    output_files.append(output_path_2)
    
    return output_files


def process_pdf_with_passes(input_path, output_base_path=None,
                            attribution_text="Dr. Tara Salman",
                            font_size=24):
    """
    Process a PDF file with two rotation passes on each page.
    
    Args:
        input_path: Path to input PDF
        output_base_path: Base path for output (if None, uses input path stem)
        attribution_text: Text to add
        font_size: Font size
    
    Returns:
        List of output file paths
    """
    if not PDF_SUPPORT:
        raise ImportError("pdf2image is required for PDF processing. Install with: uv pip install pdf2image")
    
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"PDF not found: {input_path}")
    
    if output_base_path is None:
        output_base_path = input_path.parent / input_path.stem
    else:
        output_base_path = Path(output_base_path)
    
    print(f"Processing PDF: {input_path.name}")
    
    # Convert PDF pages to images
    print("  Converting PDF pages to images...")
    pages = convert_from_path(str(input_path), dpi=300)
    print(f"  Found {len(pages)} pages")
    
    # Process each page with passes
    pass1_pages = []
    pass2_pages = []
    
    for i, page in enumerate(pages, 1):
        print(f"  Processing page {i}/{len(pages)}...")
        
        # Convert to RGB if needed
        if page.mode != 'RGB':
            page = page.convert('RGB')
        
        original_size = page.size
        print(f"    Original dimensions: {original_size[0]} x {original_size[1]}")
        
        # PASS 1: Rotate 90 degrees
        print(f"    Pass 1: Rotating 90 degrees...")
        rotated_90 = rotate_image(page, 90)
        print(f"      After 90° rotation: {rotated_90.size[0]} x {rotated_90.size[1]}")
        attributed_90 = add_attribution_to_image(
            rotated_90, attribution_text, font_size=font_size
        )
        pass1_pages.append(attributed_90)
        
        # PASS 2: Rotate additional 250 degrees
        print(f"    Pass 2: Rotating additional 250 degrees (340° total)...")
        rotated_340 = rotate_image(rotated_90, 250)
        print(f"      After 340° rotation: {rotated_340.size[0]} x {rotated_340.size[1]}")
        attributed_340 = add_attribution_to_image(
            rotated_340, attribution_text, font_size=font_size
        )
        pass2_pages.append(attributed_340)
    
    # Save pass 1 PDF
    output_path_1 = output_base_path.parent / f"{output_base_path.name}_pass1.pdf"
    print(f"  Saving Pass 1 PDF: {output_path_1}")
    if len(pass1_pages) > 0:
        pass1_pages[0].save(
            str(output_path_1),
            "PDF",
            resolution=300.0,
            save_all=True,
            append_images=pass1_pages[1:] if len(pass1_pages) > 1 else []
        )
        print(f"  Pass 1 saved to: {output_path_1}")
    
    # Save pass 2 PDF (copy)
    output_path_2 = output_base_path.parent / f"{output_base_path.name}_pass2.pdf"
    print(f"  Saving Pass 2 PDF: {output_path_2}")
    if len(pass2_pages) > 0:
        pass2_pages[0].save(
            str(output_path_2),
            "PDF",
            resolution=300.0,
            save_all=True,
            append_images=pass2_pages[1:] if len(pass2_pages) > 1 else []
        )
        print(f"  Pass 2 saved to: {output_path_2}")
    
    return [output_path_1, output_path_2]


def process_directory(directory_path, output_dir=None, attribution_text="Dr. Tara Salman",
                     file_patterns=None, font_size=20):
    """
    Process all images and PDFs in a directory with rotation passes.
    
    Args:
        directory_path: Directory containing files
        output_dir: Output directory (if None, creates 'attributed' subdirectory)
        attribution_text: Text to add
        file_patterns: List of file extensions to process
        font_size: Font size
    
    Returns:
        List of processed file paths
    """
    directory_path = Path(directory_path)
    
    if not directory_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory_path}")
    
    if output_dir is None:
        output_dir = directory_path / "attributed"
    else:
        output_dir = Path(output_dir)
    
    output_dir.mkdir(exist_ok=True)
    
    if file_patterns is None:
        file_patterns = ['.jpg', '.jpeg', '.png', '.pdf', '.JPG', '.JPEG', '.PNG', '.PDF']
    
    processed_files = []
    
    # Find all matching files
    files_to_process = []
    for pattern in file_patterns:
        files_to_process.extend(directory_path.glob(f"*{pattern}"))
    
    print(f"Found {len(files_to_process)} files to process")
    
    for file_path in files_to_process:
        try:
            output_base = output_dir / file_path.stem
            if file_path.suffix.lower() == '.pdf':
                result = process_pdf_with_passes(file_path, output_base, attribution_text, font_size)
            else:
                result = process_image_with_passes(file_path, output_base, attribution_text, font_size)
            processed_files.extend(result)
        except Exception as e:
            print(f"Error processing {file_path.name}: {e}")
            import traceback
            traceback.print_exc()
    
    return processed_files


def main():
    parser = argparse.ArgumentParser(
        description="Add attribution to images and PDF documents with rotation passes"
    )
    parser.add_argument(
        "input",
        help="Input file or directory path"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file or directory path (optional)"
    )
    parser.add_argument(
        "-t", "--text",
        default="Dr. Tara Salman",
        help="Attribution text (default: 'Dr. Tara Salman')"
    )
    parser.add_argument(
        "-s", "--size",
        type=int,
        default=20,
        help="Font size (default: 20)"
    )
    
    args = parser.parse_args()
    
    input_path = Path(args.input)
    
    if not input_path.exists():
        print(f"Error: Path does not exist: {input_path}")
        sys.exit(1)
    
    try:
        if input_path.is_file():
            # Process single file
            if input_path.suffix.lower() == '.pdf':
                if args.output:
                    output_base = Path(args.output).with_suffix('')
                else:
                    output_base = input_path.parent / input_path.stem
                process_pdf_with_passes(input_path, output_base, args.text, args.size)
            else:
                if args.output:
                    output_base = Path(args.output).with_suffix('')
                else:
                    output_base = input_path.parent / input_path.stem
                process_image_with_passes(input_path, output_base, args.text, args.size)
        elif input_path.is_dir():
            # Process directory
            process_directory(input_path, args.output, args.text, font_size=args.size)
        else:
            print(f"Error: Invalid path: {input_path}")
            sys.exit(1)
        
        print("\nProcessing complete!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
