from ultralytics import YOLO
import os

def main():
    print("==========================================")
    print("Initiating Custom YOLOv8 Wildlife Training")
    print("==========================================\n")

    # Define the absolute path to your dataset YAML file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_yaml = os.path.join(current_dir, "datasets", "african-wildlife", "african-wildlife.yaml")

    if not os.path.exists(dataset_yaml):
        print(f"ERROR: Could not find dataset YAML at: {dataset_yaml}")
        return

    print(f"Found dataset configuration: {dataset_yaml}")
    print("Loading base YOLOv8 nano model (yolov8n.pt)...")
    
    # 1. Load a pretrained base model (recommended for training)
    model = YOLO("yolov8n.pt")

    print("\nStarting the training process...")
    print("This may take a while depending on your computer's GPU/CPU.")
    
    # 2. Train the model
    # We use 50 epochs as a solid baseline. It will auto-stop early if it stops improving.
    results = model.train(
        data=dataset_yaml,
        epochs=50,          # Number of training loops
        imgsz=640,          # Image size 
        batch=16,           # Slices of data processed at a time
        name="wildlife_custom_model" # Folder name where results are saved
    )

    print("\n==========================================")
    print("🚀 TRAINING COMPLETE!")
    print("==========================================")
    print("Your new custom model has been saved in the 'runs/detect/wildlife_custom_model/weights' folder.")
    print("Look for the file named 'best.pt'!\n")
    print("To use it, update edge_device/config.py from:")
    print("   MODEL_PATH = os.path.join(BASE_DIR, '../models/yolov8n.pt')")
    print("To:")
    print("   MODEL_PATH = os.path.join(BASE_DIR, '../runs/detect/wildlife_custom_model/weights/best.pt')")

if __name__ == '__main__':
    # Required for Windows multiprocessing compatibility
    main()
