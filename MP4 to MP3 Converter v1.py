import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import subprocess
import threading
import os

root = tk.Tk()
root.title("MP4 to MP3 Converter")

file_paths = []
album_art_path = ""
bitrate = tk.StringVar(value="128k")  # Default bitrate

def select_files():
    global file_paths
    file_paths = filedialog.askopenfilenames(filetypes=[("MP4 Files", "*.mp4")])
    file_list_text.config(state=tk.NORMAL)
    file_list_text.delete(1.0, tk.END)
    file_list_text.insert(tk.END, "\n".join(file_paths))
    file_list_text.config(state=tk.DISABLED)
    success_label.config(text="")
    progress_var.set(0)
    progress_bar['maximum'] = len(file_paths)

def select_album_art():
    global album_art_path
    album_art_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    album_art_label.config(text=album_art_path)

def convert_to_mp3():
    global file_paths, album_art_path
    if not file_paths:
        messagebox.showwarning("No files selected", "Please select MP4 files to convert.")
        return

    prefix = filename_prefix_entry.get().strip()
    if not prefix:
        messagebox.showwarning("No prefix entered", "Please enter a filename prefix.")
        return

    for idx, file_path in enumerate(file_paths):
        output_file = os.path.join(os.path.dirname(file_path), f"{prefix}_{idx}.mp3")
        if album_art_path:
            command = f"ffmpeg -i \"{file_path}\" -i \"{album_art_path}\" -map 0:0 -map 1:0 -c copy -id3v2_version 3 -metadata:s:v title=\"Album cover\" -metadata:s:v comment=\"Cover (front)\" -b:a {bitrate.get()} \"{output_file}\""
        else:
            command = f"ffmpeg -i \"{file_path}\" -vn -b:a {bitrate.get()} \"{output_file}\""
        
        try:
            subprocess.call(command, shell=True)
            status_label.config(text=f"Converted: {file_path}")
            progress_var.set(idx + 1)
        except Exception as e:
            messagebox.showerror("Conversion failed", f"An error occurred: {e}")

    success_label.config(text="All conversions completed!")

def convert_to_mp3_async():
    thread = threading.Thread(target=convert_to_mp3)
    thread.start()

def clear_fields():
    global file_paths, album_art_path
    file_paths = []
    album_art_path = ""
    file_list_text.config(state=tk.NORMAL)
    file_list_text.delete(1.0, tk.END)
    file_list_text.config(state=tk.DISABLED)
    album_art_label.config(text="")
    success_label.config(text="")
    progress_var.set(0)
    status_label.config(text="")

def open_output_folder():
    if file_paths:
        output_dir = os.path.dirname(file_paths[0])
        if os.path.isdir(output_dir):
            subprocess.call(f'explorer "{output_dir}"', shell=True)
        else:
            messagebox.showwarning("Output Directory Not Found", "The output directory could not be found.")
    else:
        messagebox.showwarning("No files selected", "Please select MP4 files to convert.")

# GUI Components
file_list_label = tk.Label(root, text="File List")
file_list_text = tk.Text(root, height=10, state=tk.DISABLED)
filename_prefix_label = tk.Label(root, text="Filename prefix (0.mp3, 1.mp3, ...)")
filename_prefix_entry = tk.Entry(root)
select_button = tk.Button(root, text="Select MP4 Files", command=select_files)
convert_button = tk.Button(root, text="Convert to MP3", command=convert_to_mp3_async)
open_button = tk.Button(root, text="Open Output Folder", command=open_output_folder)
album_art_label = tk.Label(root, text="")
select_album_art_button = tk.Button(root, text="Select Album Art", command=select_album_art)
status_label = tk.Label(root, text="")
success_label = tk.Label(root, text="")

progress_var = tk.IntVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)

# Bitrate selection
bitrate_label = tk.Label(root, text="Select Bitrate:")
bitrates = ["96k", "112k", "128k", "160k", "192k", "256k", "320k"]
bitrate_frame = tk.Frame(root)
for br in bitrates:
    rb = tk.Radiobutton(bitrate_frame, text=br, variable=bitrate, value=br)
    rb.pack(side=tk.LEFT)

# Layout
file_list_label.grid(row=0, column=0, pady=5, padx=10, sticky="w")
file_list_text.grid(row=1, column=0, pady=5, padx=10, sticky="nsew", columnspan=4)
filename_prefix_label.grid(row=2, column=0, pady=5, padx=10, sticky="w")
filename_prefix_entry.grid(row=3, column=0, pady=5, padx=10, sticky="ew", columnspan=4)
bitrate_label.grid(row=4, column=0, pady=5, padx=10, sticky="w")
bitrate_frame.grid(row=5, column=0, pady=5, padx=10, sticky="ew", columnspan=4)
album_art_label.grid(row=6, column=0, pady=5, padx=10, sticky="w", columnspan=4)
select_album_art_button.grid(row=7, column=3, pady=5, padx=10, sticky="e")
progress_bar.grid(row=8, column=0, pady=5, padx=10, sticky="ew", columnspan=4)
select_button.grid(row=9, column=0, pady=5, padx=10, sticky="w")
convert_button.grid(row=9, column=1, pady=5, padx=10, sticky="w")
open_button.grid(row=9, column=2, pady=5, padx=10, sticky="w")
status_label.grid(row=10, column=0, pady=5, padx=10, sticky="w", columnspan=4)
success_label.grid(row=11, column=0, pady=5, padx=10, sticky="w", columnspan=4)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

root.mainloop()
