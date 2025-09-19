import yt_dlp
import os
from urllib.parse import urlparse
from getpass import getpass

def download_video(url, output_path=None, username=None, password=None):
    # Validate URL
    if not url or not urlparse(url).scheme:
        raise ValueError("Invalid URL")

    # Configure options for yt-dlp
    ydl_opts = {
        'format': 'best',
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'outtmpl': '%(title)s.%(ext)s',
        'quiet': False,
        'no_warnings': False,
        # Remove cookiesfrombrowser and add direct authentication
        'username': username,
        'password': password,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    }
    
    if output_path:
        os.makedirs(output_path, exist_ok=True)
        ydl_opts['outtmpl'] = os.path.join(output_path, '%(title)s.%(ext)s')

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"Downloading: {info.get('title', 'Untitled')}")
            ydl.download([url])
        print("✓ Download completed successfully!")
    except Exception as e:
        print(f"✗ An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        print("Supported platforms: YouTube, Instagram, Twitter, TikTok, Vimeo, and more")
        video_url = input("Enter video URL: ").strip()
        
        # Ask for credentials if it's an Instagram URL
        username = None
        password = None
        if 'instagram.com' in video_url:
            print("\nInstagram login required:")
            username = input("Username: ").strip()
            password = getpass("Password: ")
        
        output_path = "downloads"
        download_video(video_url, output_path, username, password)
    except KeyboardInterrupt:
        print("\n✗ Download cancelled by user")
    except ValueError as e:
        print(f"✗ Error: {str(e)}")