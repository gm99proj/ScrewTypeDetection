import cv2
import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import numpy as np

# Global variables
capturing = False
capture_count = 0
save_folder = "captured_raw_photos"

# Screw types
screw_types = {
    "1": "Socket head cap screw",
    "2": "Flat head socket screw",
    "3": "Wood screw",
    "4": "Sheet metal screw"
}

# Background types
background_types = {
    "b": "Black",
    "w": "White"
}

# Create folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

def start_capture():
    global capturing, capture_count
    capturing = True
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Could not access the webcam.")
        return

    while capturing:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image")
            break

        # Display the original frame
        cv2.imshow("Webcam (Original)", frame)

        # Check for key press
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('c'):  # Press 'c' to capture an image
            capture_count += 1
            background_choice = simpledialog.askstring("Background Type", "Choose background type:\n'b' for Black\n'w' for White")
            if background_choice not in background_types:
                print("Invalid background choice, image not saved.")
                continue
            
            screw_choice = simpledialog.askstring("Screw Type", "Choose screw type:\n1: Socket head cap screw\n2: Flat head socket screw\n3: Wood screw\n4: Sheet metal screw")
            
            if screw_choice in screw_types:
                background_folder = os.path.join(save_folder, background_types[background_choice])
                if not os.path.exists(background_folder):
                    os.makedirs(background_folder)
                
                screw_type = screw_types[screw_choice]
                screw_folder = os.path.join(background_folder, screw_type)
                if not os.path.exists(screw_folder):
                    os.makedirs(screw_folder)
                
                filename = os.path.join(screw_folder, f"{screw_type}_image_{capture_count}.jpg")
                cv2.imwrite(filename, frame)
                print(f"Captured: {filename}")
            else:
                print("Invalid screw type choice, image not saved.")
        
        elif key == ord('e'):  # Press 'e' to stop capture
            capturing = False

    cap.release()
    cv2.destroyAllWindows()

def on_keypress(event):
    if event.char == 's':  # Press 's' to start capture
        start_capture()

# Create the main window
window = tk.Tk()
window.title("Capture Multiple Images with Webcam")

# Add instructions label
instructions = tk.Label(window, text="Press 's' to start the webcam, 'c' to capture, and 'e' to stop.")
instructions.pack(pady=20)

# Bind the key press event to the window
window.bind("<Key>", on_keypress)

# Start the Tkinter event loop
window.mainloop()
