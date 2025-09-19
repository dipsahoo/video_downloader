import yt_dlp
import os
from urllib.parse import urlparse

def download_video(url, output_path=None):
    # Validate URL
    if not url or not urlparse(url).scheme:
        raise ValueError("Invalid YouTube URL")

    # Configure options for yt-dlp
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',  # Changed format
        'merge_output_format': 'mp4',
        'noplaylist': True,
        'outtmpl': '%(title)s.%(ext)s',
        'postprocessors': [{  # Add postprocessors for audio
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }
    if output_path:
        # Ensure output folder exists
        os.makedirs(output_path, exist_ok=True)
        ydl_opts['outtmpl'] = os.path.join(output_path, '%(title)s.%(ext)s')

    try:
        # Create a YoutubeDL object with the options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("✓ Download completed successfully!")
    except Exception as e:
        print(f"✗ An error occurred: {str(e)}")

if __name__ == "__main__":
    try:
        video_url = input("Enter YouTube URL: ").strip()
        output_path = "downloads"
        download_video(video_url, output_path)
    except KeyboardInterrupt:
        print(" Download cancelled by user")
    except ValueError as e:
        print(f" Error: {str(e)}")