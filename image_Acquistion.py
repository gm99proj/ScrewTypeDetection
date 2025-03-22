import cv2
import tkinter as tk
from tkinter import messagebox
import os

# Global variables
capturing = False
capture_count = 0
save_folder = "captured_raw_photos"

# Create folder if it doesn't exist
if not os.path.exists(save_folder):
    os.makedirs(save_folder)

# Function to start the webcam capture and take multiple pictures
def start_capture():
    global capturing, capture_count
    capturing = True

    # Start the webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        messagebox.showerror("Error", "Could not access the webcam.")
        return

    while capturing:
        ret, frame = cap.read()
        if ret:
            # Display the frame in a window
            cv2.imshow("Webcam", frame)

            # Check for key press to capture a photo (press 'c' to capture photo)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('c'):  # Press 'c' to capture an image
                capture_count += 1
                image_filename = os.path.join(save_folder, f"captured_image_{capture_count}.jpg")
                cv2.imwrite(image_filename, frame)
                print(f"Captured: {image_filename}")
                messagebox.showinfo("Captured", f"Image {capture_count} saved as {image_filename}")
        
            # Check for key press to stop (press 'e' to end capture)
            if key == ord('e'):  # Press 'e' to stop capture
                capturing = False

    # Release the webcam and close the window
    cap.release()
    cv2.destroyAllWindows()

# Function to handle keypress events
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
