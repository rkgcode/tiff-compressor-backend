from PIL import Image, ImageEnhance
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
            img_resized = enhancer.enhance(1.5)  # Increase sharpness (1.5x)

            # Optionally, set DPI to 300 for better clarity in text
            img_resized.info['dpi'] = (1200, 1200)
            
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


# its working very well -assume as final