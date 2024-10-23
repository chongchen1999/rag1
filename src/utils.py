# utils.py
import tempfile
import hashlib
import os

def handle_file_upload(uploaded_files):
    """Handle file uploads and return temporary directory path."""
    if uploaded_files:
        temp_dir = tempfile.mkdtemp()
        for uploaded_file in uploaded_files:
            file_path = os.path.join(temp_dir, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
        return temp_dir
    return None

def get_files_hash(files):
    """Calculate MD5 hash for uploaded files."""
    hash_md5 = hashlib.md5()
    for file in files:
        file_bytes = file.read()
        hash_md5.update(file_bytes)
        file.seek(0)  # Reset file pointer
    return hash_md5.hexdigest()