import cv2
import numpy as np

def calculate_sharpness(image):
    """Measure the sharpness using the Laplacian variance."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    return laplacian.var()  # Higher variance = sharper image

# Open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Measure sharpness
    sharpness = calculate_sharpness(frame)
    cv2.putText(frame, f"Sharpness: {sharpness:.2f}", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Focus Test", frame)

    # Stop on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()