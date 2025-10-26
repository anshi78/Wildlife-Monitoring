# --- Cloud Backend Configuration ---
API_URL = "http://127.0.0.1:8000"
# This is the "Ghost-Fix": Hardcode the key to match the server
API_KEY = "MySuperSecretKey2025" 
DEVICE_ID = "device_001_dehradun"

# --- Local Storage Configuration ---
DB_FILE = "local_detections.db"
IMG_DIR = "detected_images"

# --- Model & Detection Configuration ---
# IMPORTANT: Change this to point to your custom-trained .pt file
MODEL_PATH = "models/yolov8n.pt" 

# IMPORTANT: Change this to match the classes of your custom model
SPECIES_LIST = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

# Example for your custom model:
# SPECIES_LIST = ['deer', 'boar', 'elephant', 'monkey', 'leopard', 'person']

CONFIDENCE_THRESHOLD = 0.50 # Only detect objects with 50% or higher confidence
MOTION_THRESHOLD = 1000     # Pixel area threshold to trigger detection