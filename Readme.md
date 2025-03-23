# TIFF File Compressor API

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Status](https://img.shields.io/badge/status-active-success)

Professional TIFF image compression API with quality preservation. Reduce TIFF file sizes while maintaining image quality.

## 🚀 Features

- **Intelligent Compression**: Advanced algorithms to reduce file size while preserving quality
- **Customizable Parameters**: Fine-tune compression settings to meet your needs
- **Quality Preservation**: Maintain image integrity during compression
- **Fast Processing**: Quick compression response times
- **Flexible Options**: Adjust DPI, sharpness, contrast, and more
- **Secure Processing**: Safe and secure file handling
- **REST Architecture**: Simple and standard API interface
- **Detailed Documentation**: Comprehensive guides and examples

## 📋 API Endpoints

### 1. Get API Information
```http
GET /
```
Returns API information and available endpoints.

#### Response Example
```json
{
    "message": "Welcome to TIFF Compressor API",
    "version": "1.0.0",
    "endpoints": {
        "/compress": "POST endpoint to compress TIFF files",
        "/": "This information endpoint"
    }
}
```

### 2. Compress TIFF File
```http
POST /compress
```

#### Parameters

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| file | File | Yes | - | TIFF file to compress (.tiff, .tif) |
| target_size_kb | Integer | Yes | - | Target file size in kilobytes |
| min_size_percentage | Float | No | 0.3 | Minimum size percentage (0.1-1.0) |
| scale_factor | Float | No | 0.9 | Initial scale factor (0.1-1.0) |
| sharpness_factor | Float | No | 1.5 | Sharpness enhancement (0.1-3.0) |
| contrast_factor | Float | No | 1.5 | Contrast enhancement (0.1-3.0) |
| blur_radius | Float | No | 0.1 | Gaussian blur radius (0.0-2.0) |
| dpi | Integer | No | 300 | Output image DPI |

## 💻 Code Examples

### Python
```python
import requests

url = "https://tiff-file-compressor.p.rapidapi.com/compress"

headers = {
    "X-RapidAPI-Key": "YOUR_API_KEY",
    "X-RapidAPI-Host": "tiff-file-compressor.p.rapidapi.com"
}

files = {
    'file': ('image.tiff', open('image.tiff', 'rb'), 'image/tiff')
}

data = {
    'target_size_kb': 1000,
    'min_size_percentage': 0.3,
    'scale_factor': 0.9,
    'sharpness_factor': 1.5,
    'contrast_factor': 1.5,
    'blur_radius': 0.1,
    'dpi': 300
}

response = requests.post(url, headers=headers, files=files, data=data)

# Save the compressed file
with open('compressed_image.tiff', 'wb') as f:
    f.write(response.content)
```

### Node.js
```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const form = new FormData();
form.append('file', fs.createReadStream('image.tiff'));
form.append('target_size_kb', '1000');

const options = {
    method: 'POST',
    url: 'https://tiff-file-compressor.p.rapidapi.com/compress',
    headers: {
        'X-RapidAPI-Key': 'YOUR_API_KEY',
        'X-RapidAPI-Host': 'tiff-file-compressor.p.rapidapi.com',
        ...form.getHeaders()
    },
    data: form
};

axios.request(options)
    .then(response =&gt; {
        fs.writeFileSync('compressed.tiff', response.data);
    })
    .catch(error =&gt; console.error(error));
```

## 🎯 Use Cases

1. **Document Management Systems**
   - Reduce storage costs
   - Optimize document archives
   - Maintain document quality

2. **Professional Photography**
   - Compress high-resolution images
   - Preserve image details
   - Optimize for web/print

3. **Healthcare Imaging**
   - Compress medical images
   - Maintain diagnostic quality
   - Reduce storage requirements

4. **Technical Documentation**
   - Compress technical drawings
   - Preserve detail accuracy
   - Reduce file sizes

## ⚙️ Parameter Guidelines

### Optimization Tips

1. **For Maximum Compression**
   ```json
   {
       "target_size_kb": desired_size,
       "min_size_percentage": 0.3,
       "scale_factor": 0.8,
       "sharpness_factor": 1.8,
       "contrast_factor": 1.6
   }
   ```

2. **For Best Quality**
   ```json
   {
       "target_size_kb": desired_size,
       "min_size_percentage": 0.5,
       "scale_factor": 0.95,
       "sharpness_factor": 1.3,
       "contrast_factor": 1.3
   }
   ```

## 🔧 Error Handling

Common error responses:

```json
{
    "detail": "Only TIFF files are supported"
}
```
```json
{
    "detail": "File size exceeds maximum limit"
}