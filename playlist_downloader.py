import tkinter as tk
from tkinter import messagebox
from yt_dlp import YoutubeDL

def download_playlist():
    url = entry_url.get().strip()
    resolution = resolution_var.get()

    if not url:
        messagebox.showerror("Error", "Please enter a playlist URL")
        return

    # صيغة التحميل
    if resolution == "best":
        fmt = "bestvideo+bestaudio/best"
    else:
        fmt = f"bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]"

    ydl_opts = {
        "format": fmt,
        "outtmpl": "%(playlist_index)s - %(title)s.%(ext)s",
        "merge_output_format": "mp4",
        "postprocessors": [
            {  
                "key": "FFmpegVideoConvertor",
                "preferedformat": "mp4"   # تحويل الفيديو إلى MP4
            }
        ],
        # نجبر ffmpeg يحول H.264 + AAC
        "postprocessor_args": [
            "-c:v", "libx264",
            "-c:a", "aac",
            "-b:a", "192k"
        ]
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        messagebox.showinfo("Done", "Download and conversion completed successfully ✅")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# ---------------- User Interface ---------------- #
root = tk.Tk()
root.title("YouTube Playlist Downloader")
root.geometry("400x250")

tk.Label(root, text="Playlist URL:", font=("Arial", 12)).pack(pady=5)
entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=5)

tk.Label(root, text="Select Quality:", font=("Arial", 12)).pack(pady=5)
resolution_var = tk.StringVar(value="720")
res_options = ["best", "1080", "720", "480"]
tk.OptionMenu(root, resolution_var, *res_options).pack(pady=5)

tk.Button(root, text="Download", font=("Arial", 14), bg="green", fg="white", command=download_playlist).pack(pady=20)

root.mainloop()
