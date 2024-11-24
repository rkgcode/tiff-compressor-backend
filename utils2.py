from PIL import Image, ImageEnhance, ImageFilter
import os

def compress_tiff_file(input_file: str, target_size_kb: int) -> str:
    """
    Compress a TIFF file iteratively until it fits within the target size.

    Args:
        input_file (str): Path to the input TIFF file.
        target_size_kb (int): Target size in KB.

    Returns:
        str: Path to the compressed TIFF file.
    """
    output_file = f"compressed_{os.path.basename(input_file)}"
    compression = "tiff_lzw"  # Use LZW compression
    scale_factor = 0.9  # Start with a slight scaling down

    while True:
        # Open the TIFF file
        with Image.open(input_file) as img:
            # Scale down the image size
            new_size = (int(img.width * scale_factor), int(img.height * scale_factor))
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS)  # Resizing with high quality
            
            # Apply sharpening filter to enhance text quality
            enhancer = ImageEnhance.Sharpness(img_resized)
            img_resized = enhancer.enhance(2.0)  # Increase sharpness for better clarity
            
            # Apply contrast enhancement to improve text visibility
            contrast_enhancer = ImageEnhance.Contrast(img_resized)
            img_resized = contrast_enhancer.enhance(1)  # Increase contrast to make text stand out more

            # Apply slight denoising (Gaussian Blur) to remove noise and smooth the image
            img_resized = img_resized.filter(ImageFilter.GaussianBlur(radius=0.1))  # Small blur to reduce noise

            # Optionally, set DPI to 1200 for better clarity in text
            img_resized.info['dpi'] = (300, 300)
            
            # Strip metadata (e.g., EXIF, ICC profile)
            img_resized.info = {}
            
            # Save the image with compression
            img_resized.save(output_file, format="TIFF", compression=compression)
        
        # Check the file size
        output_size_kb = os.path.getsize(output_file) / 1024
        if output_size_kb <= target_size_kb or scale_factor <= 0.1:
            break  # Exit if within target size or scale factor is too low
        
        # Further reduce resolution
        scale_factor *= 0.99

    return output_file