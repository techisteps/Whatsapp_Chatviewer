## WhatsApp Chat Ingestor
A Python-based utility to automate the ingestion of exported WhatsApp chat archives into local SQLite databases. This script handles zip extraction, message parsing using Regular Expressions, and automated organization of media files and processed archives.

## Project Structure
```text
.
├── inbox/            # Place new WhatsApp .zip exports here
├── process/          # Temporary workspace for extraction
├── archive/          # Successfully processed .zip files are moved here
├── db/               # SQLite databases named by MD5 hash of original zip
├── media/            # Chat-specific folders for photos/videos
├── Utils/
│   └── utils_ingestions.py
└── README.md
```

## Functionality
1. Atomic Processing: Moves one `.zip` file at a time from `inbox` to `process` to ensure system stability.
2. MD5 Identification: Uses the MD5 hash of the original filename for the database name to ensure uniqueness and consistency.
3. Data Extraction: Parses the exported text file into a structured SQLite table (`messages`) containing timestamps, senders, and message content.
4. Media Organization: Automatically detects media files within the archive and moves them to a dedicated subfolder in `media/` named after the chat archive.
5. Safe File Handling: Utilizes Python context managers to prevent "File in Use" errors on Windows, ensuring all file locks are released before moving or deleting files. 


## Requirements
Python Version: 3.8+ (Tested on Python 3.13 in 2026).
Standard Libraries: `sqlite3`, `zipfile`, `hashlib`, `shutil`, `re`, `pathlib`. 

## Setup & Usage
1. Preparation  
Place your exported WhatsApp `.zip` files into the `inbox` folder. Do not extract them manually.

2. Running the Script  
- - Run the script from the project root directory using the following command: 
    ```bash
    python utils/utils_ingestions.py
    ```
    >> Note: No command-line parameters are required as the script automatically detects files in the `inbox`.

- - Running as a Module (Optional)  
    If you plan to expand the script into a larger package, it is a best practice to run it as a module:
    ```bash
    python -m utils.utils_ingestions
    ```
    >> Note: This requires an empty `__init__.py` file inside the `utils/` folder.

3. Output  
**Database**: Check the `db/` folder for a `.sqlite` file.  
**Media**: Check the `media/[Chat Name]/` folder for images, videos, and PDFs.  
**Archive**: The original zip is moved to `archive/` for safekeeping.  


## Database Schema
The generated SQLite databases contain a table named messages with the following columns:  

| Column | Type | Description |
|---|---|---|
timestamp   | TEXT | Date and time of the message
sender	    | TEXT | Name of the person who sent the message
content	    | TEXT | The actual message text or media reference

## Troubleshooting
- PermissionError (WinError 32): This error is common on Windows if a file is still open in another program (like a PDF viewer or text editor). Ensure the zip is not open elsewhere before running the script. The script is designed with context managers to minimize this risk.
- Parsing Issues: WhatsApp export formats can vary slightly by region or device (iOS vs. Android). If messages are not appearing in the DB, check if your chat timestamp matches the regex pattern in `utils_ingestions.py`.