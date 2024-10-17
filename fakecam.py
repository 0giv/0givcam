import cv2
import os
import pyvirtualcam
from keyboard import is_pressed
from time import sleep


def multivideo(video_folder, delay=33):  
    video_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]
    video_index = 0
    video_file = os.path.join(video_folder, video_files[video_index])
    
    cap = cv2.VideoCapture(video_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    with pyvirtualcam.Camera(width=width, height=height, fps=30) as cam:
        print(f'Virtual camera: {cam.device}')
        
        while True:
            ret, frame = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            cam.send(frame_rgb)

            
            cv2.waitKey(delay)  

            # if is_pressed('q'):
            #     video_index = (video_index + 1) % len(video_files)
            #     break

def video(video_file, delay=33):  
    cap = cv2.VideoCapture(video_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    with pyvirtualcam.Camera(width=width, height=height, fps=30) as cam:
        print(f'Virtual camera: {cam.device}')
        while True:
            ret, frame = cap.read()

            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0) 
                continue  

            
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            cam.send(frame_rgb)

            cam.sleep_until_next_frame()

            if cv2.waitKey(delay) & 0xFF == ord('q'):
                break
