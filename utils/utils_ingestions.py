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
MEDIA_DIR = BASE_DIR / "media"

for d in [PROCESS, ARCHIVE, MEDIA_DIR]: d.mkdir(exist_ok=True)

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
    """Extracts zip, parses text, and stores in SQLite."""
    db_name = f"{get_md5_filename(zip_path.name)}.sqlite"
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # Create table for messages
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages 
                     (timestamp TEXT, sender TEXT, content TEXT)''')

    chat_specific_media = MEDIA_DIR / zip_path.stem
    chat_specific_media.mkdir(exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(PROCESS)
        files = zip_ref.namelist()
        
        # Identify text file (usually _chat.txt or WhatsApp Chat with...txt)
        txt_files = [f for f in files if f.endswith('.txt')]
        if txt_files:
            txt_path = PROCESS / txt_files[0]
            with open(txt_path, 'r', encoding='utf-8') as f:
                for line in f:
                    # Basic WhatsApp Regex pattern (may vary by OS/Version)
                    match = re.match(r'\[?(\d{2}/\d{2}/\d{2,4},? \d{1,2}:\d{2}:\d{2})\]? (.*?): (.*)', line)
                    if match:
                        cursor.execute("INSERT INTO messages VALUES (?, ?, ?)", match.groups())
            conn.commit()
            os.remove(txt_path)

        # Move remaining media files to chat-specific folder
        for item in files:
            if not item.endswith('.txt'):
                file_in_process = PROCESS / item
                if file_in_process.exists():
                    shutil.move(str(file_in_process), str(chat_specific_media / item))

    conn.close()
    # Archive the original zip
    shutil.move(str(zip_path), str(ARCHIVE / zip_path.name))

if __name__ == "__main__":
    current_zip = move_one_to_process()
    if current_zip:
        print(f"Processing: {current_zip.name}")
        ingest_to_sqlite(current_zip)
    else:
        print("No files to process in inbox.")
