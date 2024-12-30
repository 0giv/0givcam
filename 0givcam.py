import tkinter as tk
from tkinter import ttk, filedialog
import cv2
import os
import pyvirtualcam
import threading

# Global variables to control video playback
running = False
skip_video = threading.Event()


def multivideo(video_folder):
    global running
    running = True
    video_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]
    video_index = 0

    if not video_files:
        print("No video files found in the folder.")
        return

    cap = cv2.VideoCapture(os.path.join(video_folder, video_files[video_index]))
    width, height = 854, 480 
    with pyvirtualcam.Camera(width=width, height=height, fps=30) as cam:
        print(f'Virtual camera: {cam.device}')

        while running:
            ret, frame = cap.read()
            if not ret or skip_video.is_set():  
                skip_video.clear()  
                video_index = (video_index + 1) % len(video_files)
                cap = cv2.VideoCapture(os.path.join(video_folder, video_files[video_index]))
                continue

            frame_resized = cv2.resize(frame, (width, height))
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            cam.send(frame_rgb)
            cam.sleep_until_next_frame()

        cap.release()


def video(video_file):
    """Play a single video."""
    global running
    running = True
    cap = cv2.VideoCapture(video_file)
    width, height = 854, 480 
    with pyvirtualcam.Camera(width=width, height=height, fps=30) as cam:
        print(f'Virtual camera: {cam.device}')
        while running:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
                continue

            frame_resized = cv2.resize(frame, (width, height))
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            cam.send(frame_rgb)
            cam.sleep_until_next_frame()

        cap.release()


def stop_video():
    """Stop video playback."""
    global running
    running = False


def skip_to_next_video():
    """Signal to skip to the next video."""
    skip_video.set()


def start_video_thread(video_file=None, video_folder=None):
    """Starts video playback in a separate thread."""
    stop_video() 
    if video_file:
        threading.Thread(target=video, args=(video_file,), daemon=True).start()
    elif video_folder:
        threading.Thread(target=multivideo, args=(video_folder,), daemon=True).start()


def select_file():
    file_path = filedialog.askopenfilename(title="Choose Video", filetypes=[("Videos", "*.mp4"), ("All Files", "*.*")])
    if file_path:
        start_video_thread(video_file=file_path)


def select_folder():
    folder_path = filedialog.askdirectory(title="Choose Video Folder")
    if folder_path:
        start_video_thread(video_folder=folder_path)


root = tk.Tk()
root.title("0giv Cam")
root.iconbitmap("ico.ico")
root.configure(bg='#0f172a')

style = ttk.Style()
style.theme_use("clam")
style.configure(
    "TButton",
    font=("Helvetica", 12, "bold"),
    padding=10,
    foreground="white",
    background="#2563eb",
    borderwidth=0,
)
style.map(
    "TButton",
    background=[("active", "#3b82f6")],
    relief=[("pressed", "groove"), ("!pressed", "flat")],
)
style.configure("TLabel", font=("Helvetica", 18, "bold"), foreground="white", background="#0f172a")

frame = ttk.Frame(root, padding=20, style="TFrame")
frame.place(relx=0.5, rely=0.5, anchor="center")


button_select_file = ttk.Button(frame, text="Select Video", command=select_file)
button_select_file.pack(pady=(0, 10), fill="x")

button_select_folder = ttk.Button(frame, text="Select Video Folder", command=select_folder)
button_select_folder.pack(pady=(0, 10), fill="x")

button_skip_video = ttk.Button(frame, text="Skip to Next Video", command=skip_to_next_video)
button_skip_video.pack(pady=(0, 10), fill="x")

button_stop_video = ttk.Button(frame, text="Stop Video", command=stop_video)
button_stop_video.pack(pady=(0, 10), fill="x")

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - 400) // 2
y_coordinate = (screen_height - 400) // 2
root.geometry(f"400x400+{x_coordinate}+{y_coordinate}")

root.mainloop()
