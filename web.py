import streamlit as st
import yt_dlp
import os
import time

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Pro Video Downloader", page_icon="🎬", layout="wide")

# Styling
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #FF4B4B; color: white; }
    .main { background-color: #f5f7f9; }
    </style>
    """, unsafe_allow_html=True)

# Create downloads directory if it doesn't exist
if not os.path.exists("downloads"):
    os.makedirs("downloads")


# --- CORE FUNCTIONS ---
def progress_hook(d):
    """Updates the UI with download progress."""
    if d['status'] == 'downloading':
        p = d.get('_percent_str', '0%').replace('%', '')
        try:
            progress_bar.progress(float(p) / 100)
        except:
            pass


def get_info(url):
    """Extracts video metadata."""
    with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
        return ydl.extract_info(url, download=False)


def download_video(url, quality_key):
    """Downloads video based on selected quality."""
    # Quality Mapping
    q_map = {
        "4K (Best)": "bestvideo+bestaudio/best",
        "1080p HD": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "Basic (MP4)": "best[ext=mp4]/best"
    }

    file_id = int(time.time())
    opts = {
        'format': q_map[quality_key],
        'outtmpl': f'downloads/%(title)s_{file_id}.%(ext)s',
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook],
    }

    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


# --- USER INTERFACE ---
st.title("🎬 Pro Video Downloader")
st.write("Download high-quality videos from YouTube, TikTok, FB, and Instagram.")

url = st.text_input("Paste Video Link:", placeholder="https://www.youtube.com/watch?v=...")

col1, col2 = st.columns([1, 1])
with col1:
    quality = st.selectbox("Select Quality", ["1080p HD", "720p", "4K (Best)", "Basic (MP4)"])

if url:
    try:
        with st.spinner("Fetching video info..."):
            meta = get_info(url)

            # Display Video Details
            with st.container():
                c1, c2 = st.columns([1, 2])
                with c1:
                    st.image(meta.get('thumbnail'), use_container_width=True)
                with c2:
                    st.subheader(meta.get('title'))
                    st.write(f"⏱ **Duration:** {meta.get('duration_string')}")
                    st.write(f"👤 **Uploader:** {meta.get('uploader')}")

            # Start Download Button
            if st.button("🚀 Start Download"):
                progress_bar = st.progress(0)
                file_path = download_video(url, quality)

                # Check if file exists (handling yt-dlp extension changes)
                if not os.path.exists(file_path):
                    file_path = file_path.rsplit('.', 1)[0] + ".mp4"

                if os.path.exists(file_path):
                    st.success("Download Complete! Click below to save.")
                    with open(file_path, "rb") as f:
                        st.download_button(
                            label="💾 Save Video to Device",
                            data=f,
                            file_name=os.path.basename(file_path),
                            mime="video/mp4"
                        )
                    # Optional: os.remove(file_path) # Uncomment to delete from server after download
                else:
                    st.error("File processing failed. Ensure FFmpeg is installed for HD.")

    except Exception as e:
        st.error(f"Error: {str(e)}")

st.markdown("---")
st.caption("Note: For 1080p+ resolutions, ensure **FFmpeg** is installed on your computer.") 