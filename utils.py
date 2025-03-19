"""
TIFF Compression Utilities
-------------------------

This module provides utilities for compressing TIFF files while preserving image quality.
It implements various image enhancement techniques to maintain visual quality
while achieving the desired file size reduction.

Functions:
    compress_tiff_file: Main function for TIFF compression with quality preservation

Author: rkgcode
Version: 1.0.0
"""

from PIL import Image, ImageEnhance, ImageFilter
import os
from typing import Union
from pathlib import Path

def compress_tiff_file(
    input_file: Union[str, Path],
    target_size_kb: int,
    min_size_percentage: float = 0.3,
    scale_factor: float = 0.9,
    sharpness_factor: float = 1.5,
    contrast_factor: float = 1.5,
    blur_radius: float = 0.1,
    dpi: int = 300
) -> str:
    """
    Compress a TIFF file while preserving image quality.
    
    This function implements an iterative compression algorithm that:
    1. Gradually reduces image dimensions while maintaining aspect ratio
    2. Applies image enhancements to preserve quality
    3. Manages DPI settings for optimal output
    4. Implements LZW compression for TIFF format
    
    Args:
        input_file (Union[str, Path]): Path to the input TIFF file
        target_size_kb (int): Desired output file size in kilobytes
        min_size_percentage (float): Minimum allowed size as percentage of original (0.1 to 1.0)
        scale_factor (float): Initial scaling factor for size reduction (0.1 to 1.0)
        sharpness_factor (float): Factor for sharpness enhancement (0.1 to 3.0)
        contrast_factor (float): Factor for contrast enhancement (0.1 to 3.0)
        blur_radius (float): Radius for Gaussian blur to reduce noise (0.0 to 2.0)
        dpi (int): DPI for the output image (> 0)
    
    Returns:
        str: Path to the compressed output file
    
    Raises:
        ValueError: If input parameters are invalid
        IOError: If file operations fail
        Image.DecompressionBombError: If input image is too large
    """
    # Input validation
    if not isinstance(target_size_kb, (int, float)) or target_size_kb <= 0:
        raise ValueError("target_size_kb must be a positive number")
    
    # Convert input_file to Path object
    input_file = Path(input_file)
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Prepare output filename
    output_file = f"compressed_{os.path.basename(input_file)}"
    compression = "tiff_lzw"  # Use LZW compression for better results
    
    # Get original image dimensions
    with Image.open(input_file) as img:
        original_width, original_height = img.size
    
    while True:
        with Image.open(input_file) as img:
            # Calculate new dimensions while respecting minimum size
            min_width = int(original_width * min_size_percentage)
            min_height = int(original_height * min_size_percentage)
            new_width = max(int(img.width * scale_factor), min_width)
            new_height = max(int(img.height * scale_factor), min_height)
            
            # Resize image using high-quality Lanczos resampling
            img_resized = img.resize(
                (new_width, new_height),
                Image.Resampling.LANCZOS
            )
            
            # Apply sharpening to enhance text and details
            enhancer = ImageEnhance.Sharpness(img_resized)
            img_resized = enhancer.enhance(sharpness_factor)
            
            # Enhance contrast for better visibility
            contrast_enhancer = ImageEnhance.Contrast(img_resized)
            img_resized = contrast_enhancer.enhance(contrast_factor)
            
            # Apply slight Gaussian blur to reduce noise
            if blur_radius > 0:
                img_resized = img_resized.filter(
                    ImageFilter.GaussianBlur(radius=blur_radius)
                )
            
            # Set DPI for better clarity
            img_resized.info['dpi'] = (dpi, dpi)
            
            # Remove metadata to reduce file size
            img_resized.info = {'dpi': (dpi, dpi)}
            
            # Save with compression
            img_resized.save(
                output_file,
                format="TIFF",
                compression=compression
            )
        
        # Check if target size achieved
        output_size_kb = os.path.getsize(output_file) / 1024
        if output_size_kb <= target_size_kb or scale_factor <= 0.1:
            break
        
        # Reduce scale factor for next iteration
        scale_factor *= 0.9
    
    return output_file