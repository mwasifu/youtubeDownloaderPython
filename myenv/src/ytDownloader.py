from pytube import YouTube
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import threading
import os


class StopableThread(threading.Thread):
    def __init__(self, target, args=()):
        super().__init__(target=target, args=args)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


# Global variable to keep track of the download thread
download_thread = None

def download_from_audio():
    global download_thread
    link = link_entry.get()
    try:
        yt = YouTube(link, on_progress_callback=progress_function)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid YouTube link")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".mp3")
    if filename:
        progress_bar.grid(row=4, columnspan=3, pady=(10, 20), padx=10, sticky="ew")  # Show the progress bar
        stop_button.grid(row=5, columnspan=3, pady=(10, 20), padx=10, sticky="ew")  # Show the stop button
        download_thread = StopableThread(target=download_audio_thread, args=(yt, filename))
        download_thread.start()

def download_audio_thread(yt, filename):
    global download_thread
    try:
        yd = yt.streams.get_audio_only()
        yd.download(output_path=filename.rsplit('/', 1)[0], filename=filename.rsplit('/', 1)[-1])
        messagebox.showinfo("Download Complete", "Audio download complete!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the download: {str(e)}")
    finally:
        download_thread = None
        reset_progress_bar()

def download_from_video():
    global download_thread
    link = link_entry.get()
    try:
        yt = YouTube(link, on_progress_callback=progress_function)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid YouTube link")
        return
    filename = filedialog.asksaveasfilename(defaultextension=".mp4")
    if filename:
        progress_bar.grid(row=4, columnspan=3, pady=(10, 20), padx=10, sticky="ew")  # Show the progress bar
        stop_button.grid(row=5, columnspan=3, pady=(10, 20), padx=10, sticky="ew")  # Show the stop button
        download_thread = StopableThread(target=download_video_thread, args=(yt, filename))
        download_thread.start()

def download_video_thread(yt, filename):
    global download_thread
    try:
        yd = yt.streams.get_highest_resolution()
        yd.download(output_path=filename.rsplit('/', 1)[0], filename=filename.rsplit('/', 1)[-1])
        messagebox.showinfo("Download Complete", "Video download complete!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during the download: {str(e)}")
    finally:
        download_thread = None
        reset_progress_bar()

def stop_download():
    global download_thread
    if download_thread:
        download_thread.stop()
        download_thread = None
        reset_progress_bar()  # Reset the progress bar
        stop_button.grid_forget()  # Hide the stop button

def enable_disable_buttons(event=None):
    if link_entry.get() and not download_thread:
        get_audio_button.config(state="normal")
        get_video_button.config(state="normal")
    else:
        get_audio_button.config(state="disabled")
        get_video_button.config(state="disabled")

def progress_function(stream, chunk, bytes_remaining):
    percent = (100 * (stream.filesize - bytes_remaining)) / stream.filesize
    # Update progress bar
    progress_bar['value'] = percent
    root.update_idletasks()  # Update GUI

def reset_progress_bar():
    progress_bar['value'] = 0
    progress_bar.grid_forget()  # Hide the progress bar
    stop_button.grid_forget()

# Create main window
root = tk.Tk()
root.title("Downloader")
root.configure(bg="#F8F8F8")

# Custom Fonts
title_font = ("Helvetica Neue", 18, "bold")
label_font = ("Helvetica Neue", 12)
button_font = ("Helvetica Neue", 12)

# Create GUI elements
ttk.Label(root, text="Enter YouTube URL:", font=label_font, background="#F8F8F8").grid(row=0, column=0, padx=10, pady=10, sticky="w")
link_entry = ttk.Entry(root, width=40, font=label_font, background="white")
link_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
link_entry.bind("<KeyRelease>", enable_disable_buttons)  # Bind the KeyRelease event

get_audio_button = ttk.Button(root, text="Get Audio", command=download_from_audio, state="disabled", style='Download.TButton')
get_audio_button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

get_video_button = ttk.Button(root, text="Get Video", command=download_from_video, state="disabled", style='Download.TButton')
get_video_button.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

progress_bar = ttk.Progressbar(root, orient='horizontal', mode='determinate', length=400, style='Download.Horizontal.TProgressbar')

stop_button = ttk.Button(root, text="Stop", command=stop_download, style='Download.TButton')

style = ttk.Style()
style.theme_use('clam')

# Apply Apple-like button styling
style.map('Download.TButton',
          foreground=[('pressed', 'white'), ('active', 'white')],
          background=[('pressed', '#007AFF'), ('active', '#007AFF')],
          font=[('pressed', button_font), ('active', button_font)])

style.configure('Download.Horizontal.TProgressbar', background='#007AFF', troughcolor='#F8F8F8', bordercolor='#F8F8F8')

# Run main event loop
root.mainloop()
