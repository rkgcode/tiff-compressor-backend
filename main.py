from fastapi import FastAPI, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from utils import compress_tiff_file

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/compress-tiff/")
async def compress_tiff(
    file: UploadFile,
    target_size_kb: int = Form(...),
    min_size_percentage: float = Form(0.3),
    scale_factor: float = Form(0.9),
    sharpness_factor: float = Form(1.5),
    contrast_factor: float = Form(1.5),
    blur_radius: float = Form(0.1),
    dpi: int = Form(300),
):
    # Save the uploaded file temporarily
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(await file.read())

    # Compress the TIFF file
    compressed_file_path = compress_tiff_file(
        temp_file_path, target_size_kb, min_size_percentage, scale_factor, sharpness_factor, contrast_factor, blur_radius, dpi
    )

    # Remove the original temporary file
    os.remove(temp_file_path)

    # Return the compressed file
    return FileResponse(compressed_file_path, media_type="image/tiff", filename=f"compressed_{file.filename}")