from PIL import Image, ImageEnhance, ImageFilter
import os

def compress_tiff_file(input_file: str, target_size_kb: int, min_size_percentage: float = 0.3,
                       scale_factor: float = 0.9, sharpness_factor: float = 1.5,
                       contrast_factor: float = 1.5, blur_radius: float = 0.1, dpi: int = 300) -> str:
    output_file = f"compressed_{os.path.basename(input_file)}"
    compression = "tiff_lzw"  # Use LZW compression

    # Open the TIFF file to determine the initial size
    with Image.open(input_file) as img:
        original_width, original_height = img.size

    while True:
        with Image.open(input_file) as img:
            # Scale down the image size, but ensure it doesn't go below the minimum size
            min_width = int(original_width * min_size_percentage)
            min_height = int(original_height * min_size_percentage)
            new_width = max(int(img.width * scale_factor), min_width)
            new_height = max(int(img.height * scale_factor), min_height)
            
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Resizing with high quality
            
            # Apply sharpening filter to enhance text quality
            enhancer = ImageEnhance.Sharpness(img_resized)
            img_resized = enhancer.enhance(sharpness_factor)  # Increase sharpness for better clarity
            
            # Apply contrast enhancement to improve text visibility
            contrast_enhancer = ImageEnhance.Contrast(img_resized)
            img_resized = contrast_enhancer.enhance(contrast_factor)  # Increase contrast to make text stand out more

            # Apply slight denoising (Gaussian Blur) to remove noise and smooth the image
            img_resized = img_resized.filter(ImageFilter.GaussianBlur(radius=blur_radius))  # Small blur to reduce noise

            # Set DPI for better clarity in text
            img_resized.info['dpi'] = (dpi, dpi)
            
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