import cv2
import os
from datetime import datetime
from ultralytics import YOLO
from edge_device import config, offline_storage

# Ensure directories and DB exist
os.makedirs(config.IMG_DIR, exist_ok=True)
offline_storage.init_db()

# Load the YOLOv8 model
print("Loading YOLOv8 model...")
model = YOLO(config.MODEL_PATH)
print("Model loaded successfully.")

# Initialize video capture (0 is the default webcam)
# For a video file, replace 0 with the file path "path/to/video.mp4"
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise IOError("Cannot open video source (webcam or file)")

# Initialize motion detection
back_sub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=True)

print("Starting wildlife detection loop... (Press 'q' to quit)")
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video stream or error. Exiting...")
        break

    # 1. Motion Detection
    fg_mask = back_sub.apply(frame)
    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    motion_detected = False
    for contour in contours:
        if cv2.contourArea(contour) > config.MOTION_THRESHOLD:
            motion_detected = True
            break
    
    if motion_detected:
        print("Motion detected! Running AI model...")
        
        # 2. AI Detection
        results = model(frame)

        for r in results:
            boxes = r.boxes
            for box in boxes:
                confidence = box.conf[0]
                
                if confidence > config.CONFIDENCE_THRESHOLD:
                    cls_id = int(box.cls[0])
                    species = config.SPECIES_LIST[cls_id]
                    
                    print(f"Detected: {species} with confidence: {confidence:.2f}")

                    timestamp = datetime.now()
                    ts_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    img_filename = f"{species}_{timestamp.strftime('%Y%m%d_%H%M%S')}.jpg"
                    img_path = os.path.join(config.IMG_DIR, img_filename)

                    # 3. Save Image and Data
                    # Draw bounding box on the frame for the saved image
                    x1, y1, x2, y2 = box.xyxy[0]
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    label = f"{species}: {confidence:.2f}"
                    cv2.putText(frame, label, (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                    # Save the image
                    cv2.imwrite(img_path, frame)
                    print(f"Saved image to {img_path}")

                    # 4. Store in local DB for sync
                    offline_storage.add_detection(species, float(confidence), ts_str, img_path, config.DEVICE_ID)

    # Display the resulting frame (optional)
    cv2.imshow('Wildlife Monitor', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()