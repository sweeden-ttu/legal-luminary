#!/usr/bin/env python3
"""
Script to add attribution to images and PDF documents using ImageMagick.
Pass 1: Rotate 90 degrees, add attribution
Pass 2: Rotate additional 250 degrees (340 total), make copy, add attribution
Each pass adds both black and white text with offset.
"""

import os
import sys
import subprocess
from pathlib import Path
import argparse


def check_imagemagick():
    """Check if ImageMagick is available."""
    try:
        result = subprocess.run(
            ['convert', '-version'],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_image_dimensions(image_path):
    """Get image dimensions using ImageMagick identify."""
    try:
        result = subprocess.run(
            ['identify', '-format', '%wx%h', str(image_path)],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            dimensions = result.stdout.strip().split('x')
            return (int(dimensions[0]), int(dimensions[1]))
    except:
        pass
    return None


def add_attribution_imagemagick(input_path, output_path, attribution_text="Dr. Tara Salman",
                                font_size=20, padding=10, x_offset=2, y_offset=3):
    """
    Add attribution to image using ImageMagick.
    Adds both black and white text with offset.
    
    Args:
        input_path: Input image path
        output_path: Output image path
        attribution_text: Text to add
        font_size: Font size
        padding: Padding from edges
        x_offset: X offset for white text
        y_offset: Y offset for white text
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    # Get dimensions
    dims = get_image_dimensions(input_path)
    if dims:
        width, height = dims
        print(f"    Image dimensions: {width} x {height}")
    
    # Calculate bottom-left position
    # ImageMagick uses top-left as origin, so bottom-left y = height - text_height - padding
    # We'll use gravity and offsets for positioning
    
    # Build ImageMagick command
    # -gravity SouthWest positions text at bottom-left
    # -annotate with offsets positions the text
    # We need to draw both black and white text
    
    # Calculate annotation offset (ImageMagick annotate uses +X+Y from gravity position)
    # Bottom-left: X = +padding, Y = -padding (negative because +Y goes down)
    annotate_offset = f"+{padding}-{padding}"
    white_annotate_offset = f"+{padding + x_offset}-{padding + y_offset}"
    
    cmd = [
        'convert',
        str(input_path),
        '-gravity', 'SouthWest',
        '-pointsize', str(font_size),
        '-fill', 'black',
        '-annotate', annotate_offset, attribution_text,
        '-fill', 'white',
        '-annotate', white_annotate_offset, attribution_text,
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise Exception(f"ImageMagick error: {result.stderr}")
        return True
    except subprocess.TimeoutExpired:
        raise Exception("ImageMagick command timed out")
    except Exception as e:
        raise Exception(f"Failed to add attribution: {e}")


def rotate_image_imagemagick(input_path, output_path, angle):
    """
    Rotate image using ImageMagick.
    
    Args:
        input_path: Input image path
        output_path: Output image path
        angle: Rotation angle in degrees
    """
    input_path = Path(input_path)
    output_path = Path(output_path)
    
    cmd = [
        'convert',
        str(input_path),
        '-rotate', str(angle),
        '-background', 'white',
        '-alpha', 'remove',
        str(output_path)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            raise Exception(f"ImageMagick rotation error: {result.stderr}")
        
        # Get new dimensions
        dims = get_image_dimensions(output_path)
        if dims:
            print(f"    After {angle}° rotation: {dims[0]} x {dims[1]}")
        
        return True
    except subprocess.TimeoutExpired:
        raise Exception("ImageMagick rotation command timed out")
    except Exception as e:
        raise Exception(f"Failed to rotate image: {e}")


def process_image_with_passes(input_path, output_base_path=None,
                              attribution_text="Dr. Tara Salman",
                              font_size=20):
    """
    Process an image file with two rotation passes.
    Pass 1: Rotate 90°, add attribution, save
    Pass 2: Rotate additional 250° (340° total), add attribution, save as copy
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"Image not found: {input_path}")
    
    if output_base_path is None:
        output_base_path = input_path.parent / input_path.stem
    else:
        output_base_path = Path(output_base_path)
    
    print(f"Processing image: {input_path.name}")
    
    # Get original dimensions
    dims = get_image_dimensions(input_path)
    if dims:
        print(f"  Original dimensions: {dims[0]} x {dims[1]}")
    
    output_files = []
    temp_dir = input_path.parent / '.attribution_temp'
    temp_dir.mkdir(exist_ok=True, exist_ok=True)
    
    try:
        # PASS 1: Rotate 90 degrees
        print("  Pass 1: Rotating 90 degrees...")
        temp_90 = temp_dir / f"{input_path.stem}_temp90{input_path.suffix}"
        rotate_image_imagemagick(input_path, temp_90, 90)
        
        # Add attribution
        output_path_1 = output_base_path.parent / f"{output_base_path.name}_pass1{input_path.suffix}"
        add_attribution_imagemagick(temp_90, output_path_1, attribution_text, font_size)
        print(f"  Pass 1 saved to: {output_path_1}")
        output_files.append(output_path_1)
        
        # PASS 2: Rotate additional 250 degrees (340 total from original)
        print("  Pass 2: Rotating additional 250 degrees (340° total)...")
        temp_340 = temp_dir / f"{input_path.stem}_temp340{input_path.suffix}"
        rotate_image_imagemagick(temp_90, temp_340, 250)
        
        # Add attribution
        output_path_2 = output_base_path.parent / f"{output_base_path.name}_pass2{input_path.suffix}"
        add_attribution_imagemagick(temp_340, output_path_2, attribution_text, font_size)
        print(f"  Pass 2 saved to: {output_path_2}")
        output_files.append(output_path_2)
        
    finally:
        # Clean up temp files
        for temp_file in temp_dir.glob(f"{input_path.stem}_temp*"):
            try:
                temp_file.unlink()
            except:
                pass
        try:
            temp_dir.rmdir()
        except:
            pass
    
    return output_files


def process_pdf_with_passes(input_path, output_base_path=None,
                            attribution_text="Dr. Tara Salman",
                            font_size=24):
    """
    Process a PDF file with two rotation passes on each page.
    Uses ImageMagick's convert to handle PDF pages.
    """
    input_path = Path(input_path)
    
    if not input_path.exists():
        raise FileNotFoundError(f"PDF not found: {input_path}")
    
    if output_base_path is None:
        output_base_path = input_path.parent / input_path.stem
    else:
        output_base_path = Path(output_base_path)
    
    print(f"Processing PDF: {input_path.name}")
    
    temp_dir = input_path.parent / '.attribution_temp'
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Convert PDF to individual page images
        print("  Converting PDF pages to images...")
        page_template = str(temp_dir / "page_%03d.png")
        
        cmd = ['convert', '-density', '300', str(input_path), page_template]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode != 0:
            raise Exception(f"PDF conversion error: {result.stderr}")
        
        page_files = sorted(temp_dir.glob("page_*.png"))
        print(f"  Found {len(page_files)} pages")
        
        pass1_pages = []
        pass2_pages = []
        
        for i, page_file in enumerate(page_files, 1):
            print(f"  Processing page {i}/{len(page_files)}...")
            
            dims = get_image_dimensions(page_file)
            if dims:
                print(f"    Original dimensions: {dims[0]} x {dims[1]}")
            
            # PASS 1: Rotate 90 degrees
            print(f"    Pass 1: Rotating 90 degrees...")
            temp_90 = temp_dir / f"page_{i:03d}_90.png"
            rotate_image_imagemagick(page_file, temp_90, 90)
            add_attribution_imagemagick(temp_90, temp_90, attribution_text, font_size)
            pass1_pages.append(temp_90)
            
            # PASS 2: Rotate additional 250 degrees
            print(f"    Pass 2: Rotating additional 250 degrees (340° total)...")
            temp_340 = temp_dir / f"page_{i:03d}_340.png"
            rotate_image_imagemagick(temp_90, temp_340, 250)
            add_attribution_imagemagick(temp_340, temp_340, attribution_text, font_size)
            pass2_pages.append(temp_340)
        
        # Combine pages back into PDFs
        print("  Combining pages into PDFs...")
        
        # Pass 1 PDF
        output_path_1 = output_base_path.parent / f"{output_base_path.name}_pass1.pdf"
        cmd1 = ['convert', '-density', '300'] + [str(p) for p in pass1_pages] + [str(output_path_1)]
        result1 = subprocess.run(cmd1, capture_output=True, text=True, timeout=300)
        if result1.returncode != 0:
            raise Exception(f"PDF creation error (pass 1): {result1.stderr}")
        print(f"  Pass 1 saved to: {output_path_1}")
        
        # Pass 2 PDF
        output_path_2 = output_base_path.parent / f"{output_base_path.name}_pass2.pdf"
        cmd2 = ['convert', '-density', '300'] + [str(p) for p in pass2_pages] + [str(output_path_2)]
        result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=300)
        if result2.returncode != 0:
            raise Exception(f"PDF creation error (pass 2): {result2.stderr}")
        print(f"  Pass 2 saved to: {output_path_2}")
        
        return [output_path_1, output_path_2]
        
    finally:
        # Clean up temp files
        for temp_file in temp_dir.glob("*"):
            try:
                temp_file.unlink()
            except:
                pass
        try:
            temp_dir.rmdir()
        except:
            pass


def process_directory(directory_path, output_dir=None, attribution_text="Dr. Tara Salman",
                     file_patterns=None, font_size=20):
    """Process all images and PDFs in a directory with rotation passes."""
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
        description="Add attribution to images and PDF documents with rotation passes (ImageMagick version)"
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
    
    # Check ImageMagick
    if not check_imagemagick():
        print("Error: ImageMagick is not installed or not in PATH.")
        print("Install ImageMagick: brew install imagemagick (macOS) or apt-get install imagemagick (Linux)")
        sys.exit(1)
    
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
