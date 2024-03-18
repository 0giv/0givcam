from tkinter import ttk, filedialog
import tkinter as tk
from fakecam import video
from fakecam import multivideo

root = tk.Tk()
root.title("0giv Cam")
root.configure(bg='#f0f0f0')
root.iconbitmap("ico.ico")
frame = ttk.Frame(root, padding="10")
frame.pack(expand=True, fill="both")

def select_file():
    file_path = filedialog.askopenfilename(title="Choose Video", filetypes=[("Videos", "*.mp4"), ("All Files", "*.*")])
    video(file_path)

def select_folder():
    folder_path = filedialog.askdirectory(title="Choose Video Folder")
    multivideo(folder_path)

button_style = ttk.Style()
button_style.configure('TButton', font=('Helvetica', 12, 'bold'))

button_select_file = ttk.Button(frame, text="Select Video", command=select_file, style='TButton')
button_select_file.pack(side="top", pady=(0, 10)) 

button_select_folder = ttk.Button(frame, text="Select Video Folder", command=select_folder, style='TButton')
button_select_folder.pack(side="top", pady=(0, 10))  


screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - 400) // 2
y_coordinate = (screen_height - 100) // 2
root.geometry(f"400x100+{x_coordinate}+{y_coordinate}")

root.mainloop()
