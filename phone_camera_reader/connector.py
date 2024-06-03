import os
import cv2
import time
from tkinter import *
import tkinter as tkinter
from tkinter import messagebox

def start_capture(url):
    global recording
    recording = True
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
            out.write(frame)
            resized_frame = cv2.resize(frame, (1000, 600))
            cv2.imshow('frame', resized_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    messagebox.showinfo("Info", "Recording stopped. Video saved as: " + filename)

def stop_capture():
    global recording
    recording = False

recording = False

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
