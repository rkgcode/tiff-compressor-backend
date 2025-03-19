"""
TIFF Compressor API
------------------

A FastAPI application that provides TIFF file compression with quality preservation.
The API allows customization of compression parameters and implements various
image enhancement techniques to maintain image quality while reducing file size.

Author: rkgcode
Version: 1.0.0
"""

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from tempfile import NamedTemporaryFile
from utils import compress_tiff_file
from pathlib import Path

# Initialize FastAPI application
app = FastAPI(
    title="TIFF Compressor API",
    description="A FastAPI service for compressing TIFF files while preserving image quality",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/compress/", 
    tags=["Compression"],
    summary="Compress TIFF file",
    response_description="Returns the compressed TIFF file",
    responses={
        200: {
            "description": "Successful compression",
            "content": {"image/tiff": {}}
        },
        400: {
            "description": "Invalid input",
            "content": {
                "application/json": {
                    "example": {"detail": "Only TIFF files are supported"}
                }
            }
        },
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "Error during compression"}
                }
            }
        }
    }
)
async def compress_tiff(
    file: UploadFile = File(..., description="TIFF file to compress"),
    target_size_kb: int = Form(..., description="Target file size in kilobytes", gt=0),
    min_size_percentage: float = Form(0.3, description="Minimum size percentage of original (0.1 to 1.0)", gt=0.1, le=1.0),
    scale_factor: float = Form(0.9, description="Initial scale factor for resizing (0.1 to 1.0)", gt=0.1, le=1.0),
    sharpness_factor: float = Form(1.5, description="Factor to enhance sharpness (0.1 to 3.0)", gt=0.1, le=3.0),
    contrast_factor: float = Form(1.5, description="Factor to enhance contrast (0.1 to 3.0)", gt=0.1, le=3.0),
    blur_radius: float = Form(0.1, description="Radius for Gaussian blur (0.0 to 2.0)", ge=0.0, le=2.0),
    dpi: int = Form(300, description="DPI for output image", gt=0)
):
    """
    Compress a TIFF file while preserving quality.
    
    The compression process includes:
    1. File validation
    2. Size reduction with quality preservation
    3. Image enhancement
    4. DPI adjustment
    
    The API will attempt to reach the target file size while maintaining
    the highest possible image quality using various enhancement techniques.
    
    Returns:
        FileResponse: Compressed TIFF file with appropriate headers
    
    Raises:
        HTTPException: If file type is invalid or compression fails
    """
    
    # Validate file type
    if not file.filename.lower().endswith(('.tiff', '.tif')):
        raise HTTPException(
            status_code=400, 
            detail="Only TIFF files are supported"
        )
    
    try:
        # Create temporary input file
        with NamedTemporaryFile(delete=False, suffix='.tiff') as temp_input:
            # Copy uploaded file content
            shutil.copyfileobj(file.file, temp_input)
            temp_input_path = temp_input.name
        
        # Create temporary output file
        with NamedTemporaryFile(delete=False, suffix='.tiff') as temp_output:
            temp_output_path = temp_output.name
        
        try:
            # Compress the file
            output_file = compress_tiff_file(
                temp_input_path,
                target_size_kb,
                min_size_percentage,
                scale_factor,
                sharpness_factor,
                contrast_factor,
                blur_radius,
                dpi
            )
            
            # Return the compressed file
            return FileResponse(
                output_file,
                media_type="image/tiff",
                filename=f"compressed_{file.filename}",
                headers={"Content-Disposition": f'attachment; filename="compressed_{file.filename}"'}
            )
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error during compression: {str(e)}"
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing file: {str(e)}"
        )
        
    finally:
        # Clean up temporary files
        file.file.close()
        if 'temp_input_path' in locals():
            try:
                os.unlink(temp_input_path)
            except:
                pass
        if 'temp_output_path' in locals():
            try:
                os.unlink(temp_output_path)
            except:
                pass

@app.get("/", 
    tags=["Root"],
    summary="API Information",
    response_description="Returns API information"
)
async def read_root():
    """
    Get API information and available endpoints.
    
    Returns:
        dict: API information including version and available endpoints
    """
    return {
        "message": "Welcome to TIFF Compressor API",
        "version": "1.0.0",
        "endpoints": {
            "/compress": "POST endpoint to compress TIFF files",
            "/": "This information endpoint"
        }
    }