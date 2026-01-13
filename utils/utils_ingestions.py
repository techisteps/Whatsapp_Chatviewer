import os
import shutil
import hashlib
import zipfile
import sqlite3
import re
from pathlib import Path

# Configuration
BASE_DIR = Path(".")
INBOX = BASE_DIR / "inbox"
PROCESS = BASE_DIR / "process"
ARCHIVE = BASE_DIR / "archive"
MEDIA_ROOT = BASE_DIR / "media"
DB_DIR = BASE_DIR / "db"

# Ensure all directories exist
for d in [PROCESS, ARCHIVE, MEDIA_ROOT, DB_DIR]:
    d.mkdir(exist_ok=True)

def get_md5_filename(filename):
    """Calculates MD5 hash of the filename string."""
    return hashlib.md5(filename.encode()).hexdigest()

def move_one_to_process():
    """Moves exactly one zip file from inbox to process folder."""
    zip_files = list(INBOX.glob("*.zip"))
    if not zip_files:
        return None
    source_path = zip_files[0]
    dest_path = PROCESS / source_path.name
    shutil.move(str(source_path), str(dest_path))
    return dest_path

def ingest_to_sqlite(zip_path):
    """Extracts zip, parses text, and stores in SQLite in /db folder."""
    # 1. Prepare DB Path
    db_filename = f"{get_md5_filename(zip_path.name)}.sqlite"
    db_path = DB_DIR / db_filename
    
    # 2. Extract and Parse
    # Use context manager to ensure ZIP is closed before media move
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(PROCESS)
        all_extracted_files = zip_ref.namelist()
    
    # Identify and process the text file
    txt_files = [f for f in all_extracted_files if f.endswith('.txt')]
    
    if txt_files:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS messages (timestamp TEXT, sender TEXT, content TEXT)')
        
        txt_path = PROCESS / txt_files[0]
        try:
            with open(txt_path, 'r', encoding='utf-8') as f:
                for line in f:
                    match = re.match(r'\[?(\d{2}/\d{2}/\d{2,4},? \d{1,2}:\d{2}:\d{2})\]? (.*?): (.*)', line)
                    if match:
                        cursor.execute("INSERT INTO messages VALUES (?, ?, ?)", match.groups())
            conn.commit()
        finally:
            conn.close() # Ensure DB handle is closed
            if txt_path.exists():
                os.remove(txt_path)

    # 3. Organize Media
    chat_media_folder = MEDIA_ROOT / zip_path.stem
    chat_media_folder.mkdir(exist_ok=True)

    # Move remaining files from process to chat-specific media folder
    for item in all_extracted_files:
        file_in_process = PROCESS / item
        if file_in_process.exists() and not item.endswith('.txt'):
            target_media_path = chat_media_folder / item
            # Create subdirectories if media has internal structure
            target_media_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_in_process), str(target_media_path))

    # 4. Cleanup: Archive the original zip
    shutil.move(str(zip_path), str(ARCHIVE / zip_path.name))

if __name__ == "__main__":
    current_zip = move_one_to_process()
    if current_zip:
        print(f"Processing: {current_zip.name}")
        try:
            ingest_to_sqlite(current_zip)
            print("Successfully processed and archived.")
        except Exception as e:
            print(f"Failed to process {current_zip.name}: {e}")
    else:
        print("No files found in inbox.")
