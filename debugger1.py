import os
import cv2
import time
from tkinter import *
import tkinter as tkinter
from tkinter import messagebox

def start_capture(url):
    global recording, paused, start_time, elapsed_pause_time, start_pause_time
    recording = True
    paused = False
    start_time = time.time()
    elapsed_pause_time = 0
    start_pause_time = 0
    cap = cv2.VideoCapture(url)
    if not cap.isOpened():
        messagebox.showerror("Error", "Failed To Open The Link")
        return
    
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f'output_{timestamp}.mp4'
    
    count = 1
    while os.path.exists(filename):
        filename = f'output_{timestamp}_{count}.mp4'
        count += 1
    
    format = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, format, 20.0, (width, height))
    
    while recording:
        ret, frame = cap.read()
        if ret:
            if not paused:
                out.write(frame)
            resized_frame = cv2.resize(frame, (1000, 600))
            
            if not paused:
                elapsed_time = time.time() - start_time - elapsed_pause_time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                time_text = f"Recording Time: {minutes:02d}:{seconds:02d}"
            else:
                time_text = f"Time: Paused"

            
            cv2.putText(resized_frame, time_text, (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(resized_frame, 'Pause/Resume (P)', (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(resized_frame, 'Stop (Q)', (30, 110), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            cv2.imshow('frame', resized_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('p'):
                if paused:
                    elapsed_pause_time += time.time() - start_pause_time
                else:
                    start_pause_time = time.time()
                paused = not paused
        else:
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Info", "Recording stopped. Video saved as: " + filename)

def camera():
    url = link_entry.get()
    if not url:
        messagebox.showerror("Error", "No Link Provided")
        return
    start_capture(url)

window = Tk()
window.minsize(height=600, width=1000)
window.maxsize(height=600, width=1000)

b = Button(window, text='Connect', command=camera)
b.pack(padx=0, pady=0)

link_entry = Entry(window, width=30, font=("Arial", 15), fg='red')
link_entry.pack(padx=0, pady=0)

window.mainloop()
