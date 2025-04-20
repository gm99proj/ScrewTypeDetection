#Import Libraries
import cv2
from ultralytics import YOLO

#Filepath of the trained model
model_path = 'models\yolov11_screwtype_trained_V2.pt'

# Load the trained model for real-time detection
model = YOLO(model_path)

# Get class names from the model
class_names = model.names

# Open the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Inference
    results = model(frame)

    max_conf = 0.0  # Track max confidence in this frame
    annotated_frame = frame.copy()

    for box in results[0].boxes:
        conf = box.conf[0].item()
        if conf >= 0.5:
            max_conf = max(max_conf, conf)

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cls = int(box.cls[0].item())
            label = f"{model.names[cls]}: {conf:.2f}"

            # Draw bounding box and label
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated_frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Show max confidence on frame
    cv2.putText(annotated_frame, f"Max Conf: {max_conf:.2f}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.imshow('YOLOv11 Real-Time Detection', annotated_frame)

    # Print it to console too (optional)
    print(f"Max confidence this frame: {max_conf:.4f}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()