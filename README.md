# 💬 WhatsApp Offline Chat Viewer

A lightweight Python application to view exported WhatsApp chat backups in a clean, professional chat layout. This tool runs locally and does not require a server, database, or internet connection.

## 📁 Project Structure

To ensure the script finds your chats and media, organize your folders as follows:

```text
/your-project-folder
│── app.py                         # The Python script
├── WhatsApp Chat with Family/     # A folder for a specific chat
│   ├── WhatsApp Chat with Family.txt
│   ├── IMG-20220302-WA0039.jpg    # Media files inside the same folder
│   └── ...
└── WhatsApp Chat with Friends/    # Another chat folder
    └── WhatsApp Chat with Friends.txt
```


# 🚀 Getting Started
1. Install Requirements
This project uses Streamlit, a minimalistic framework for building data tools in pure Python.


```bash
pip install streamlit
```


2. Run the Application
Navigate to your project directory in your terminal and run:

```bash
streamlit run app.py

# OR

uvx streamlit run app.py
```

# 🛠️ Implementation Details
## Message Parsing
The app uses Python's `re` (Regular Expression) module to break down each line of the text file into:
- Timestamp: Date and Time.
- Sender: Name or Phone Number.
- Content: The actual message or media reference.
- System Messages: Handles messages like "joined using a group link" which don't have a specific sender.

## Chat Layout Logic
- Alignment: You can enter your name in the sidebar. If a message sender matches your name, the message bubble is aligned to the right with a green background.
- Media Detection: The script automatically scans for (file attached) markers. If an image file (JPG/PNG) with the matching name is found in the folder, it is rendered directly inside the chat.
- UI: Built using Streamlit's layout columns and Markdown with unsafe_allow_html=True for custom CSS bubble styling.

## 📝 Features
- No Server: Runs on a local Python instance.
- Automated Folder Discovery: Scans all sub-folders for files matching the WhatsApp export naming template.
- Media Support: Displays images referenced in the chat.
- Clean UI: Mimics the WhatsApp web/mobile look for easier reading.