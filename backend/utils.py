"""Utility functions for the application"""
import os
from werkzeug.utils import secure_filename
from uuid import uuid4

def allowed_file(filename: str, allowed_extensions: set) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename for uploaded files"""
    file_ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else ''
    return f"{uuid4().hex}.{file_ext}"

def get_mime_type(filename: str) -> str:
    """Get MIME type based on file extension"""
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    mime_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'webp': 'image/webp',
        'pdf': 'application/pdf'
    }
    return mime_types.get(file_ext, 'application/octet-stream')

def ensure_directory_exists(directory: str) -> None:
    """Create directory if it doesn't exist"""
    os.makedirs(directory, exist_ok=True)

