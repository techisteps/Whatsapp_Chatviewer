import streamlit as st
import os
import re

# Page configuration
st.set_page_config(page_title="WhatsApp Chat Viewer", layout="wide")

def parse_line(line):
    # Regex to capture: Date, Time, Sender (optional), and Message
    pattern = r"^(\d{2}/\d{2}/\d{2}),\s(\d{2}:\d{2})\s-\s(?:([^:]+):\s)?(.*)$"
    match = re.match(pattern, line)
    if match:
        return {
            "date": match.group(1),
            "time": match.group(2),
            "sender": match.group(3) if match.group(3) else "System",
            "message": match.group(4)
        }
    return None

def display_chat(folder_path, file_name, your_name):
    full_path = os.path.join(folder_path, file_name)
    with open(full_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    for line in lines:
        data = parse_line(line.strip())
        if not data: continue

        is_me = data['sender'] == your_name
        # Layout: Use columns to push "Me" messages to the right
        col1, col2 = st.columns([1, 1])
        
        with (col2 if is_me else col1):
            bg_color = "#dcf8c6" if is_me else "#ffffff"
            align = "right" if is_me else "left"
            
            # Check for media
            message_content = data['message']
            media_html = ""
            if "(file attached)" in message_content:
                file_name_only = message_content.replace(" (file attached)", "").strip()
                media_path = os.path.join(folder_path, file_name_only)
                if os.path.exists(media_path):
                    if file_name_only.lower().endswith(('.png', '.jpg', '.jpeg')):
                        st.image(media_path, width=250)
                    else:
                        st.caption(f"📎 {file_name_only}")

            # Message Bubble
            st.markdown(f"""
                <div style="background-color:{bg_color}; padding:10px; border-radius:10px; 
                            margin:5px; text-align:left; border: 1px solid #ddd;">
                    <small style="color:gray;">{data['sender']} • {data['time']}</small>
                    <p style="margin:0; color:black;">{message_content}</p>
                </div>
            """, unsafe_allow_html=True)

# Sidebar UI
st.sidebar.title("💬 Chat Browser")
your_name = st.sidebar.text_input("Enter your name/number (to align right)", value="Jai")

# Find folders containing chat files
folders = [f for f in os.listdir('.') if os.path.isdir(f)]
chat_folders = []
for folder in folders:
    if any("WhatsApp Chat with" in f for f in os.listdir(folder)):
        chat_folders.append(folder)

selected_folder = st.sidebar.selectbox("Select Chat Folder", chat_folders)

if selected_folder:
    chat_file = [f for f in os.listdir(selected_folder) if "WhatsApp Chat with" in f][0]
    st.title(f"Reading: {selected_folder}")
    display_chat(selected_folder, chat_file, your_name)
