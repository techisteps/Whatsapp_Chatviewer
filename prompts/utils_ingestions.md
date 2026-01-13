# Solution

I have a folder with all the WhatsApp chat files in Zip format. I want to ingest them into a SQLite database. I need to create a python script to do this.

## Folder structure:
```text
/inbox
├── WhatsApp Chat with Family.zip
├── WhatsApp Chat with Friends.zip
└── WhatsApp Chat with Work.zip
/process
/archive
/Utils
└── utils_ingestions.py
```


## Functionality:

The script should be able to read the archive files and store the messages in the SQLite database.
New archive files will be placed in the `inbox` folder and the script should copy one file at a time and place it in `process` folder. Then the script will read the messages from txt file and store in SQLite DB.

## Steps:

1. Create a function to copy one file at a time from `inbox` folder and place it in `process` folder.
2. Create a function to extract the archive in `process` folder and read the txt file and store the messages in the SQLite database.
3. After successfully reading the txt file, move other media files to chat specific folder and move respective inbox zip archive to `archive` folder.
4. Keep DB file name as MD5 hash of the zip archive file name. Ingest each line of the txt file and store in DB.
