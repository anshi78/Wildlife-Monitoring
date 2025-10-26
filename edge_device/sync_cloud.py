import requests
import time
import schedule
import os
from edge_device import config, offline_storage

def sync_detections_to_cloud():
    """Fetches unsynced detections and uploads them to the cloud backend."""
    print("Checking for unsynced detections...")
    try:
        unsynced = offline_storage.get_unsynced_detections()
    except Exception as e:
        print(f"Error reading local database: {e}")
        return

    if not unsynced:
        print("No new detections to sync.")
        return

    print(f"Found {len(unsynced)} detections to sync.")
    headers = {"X-API-KEY": config.API_KEY}

    for detection in unsynced:
        detection_id, species, confidence, timestamp, image_path, device_id = detection
        
        # Check if image file exists before trying to send
        if not os.path.exists(image_path):
            print(f"Image not found for detection ID {detection_id} at {image_path}. Marking as synced to avoid retry.")
            offline_storage.mark_as_synced(detection_id)
            continue
            
        try:
            with open(image_path, 'rb') as img_file:
                payload = {
                    "species": species,
                    "confidence": confidence,
                    "timestamp": timestamp,
                    "device_id": device_id,
                    "location": "Dehradun, India" # You can make this dynamic
                }
                
                files = {"file": (os.path.basename(image_path), img_file, "image/jpeg")}
                
                # Corrected: Added trailing slash to the URL
                api_endpoint = f"{config.API_URL}/upload_detection/"
                
                response = requests.post(
                    api_endpoint,
                    headers=headers,
                    data=payload,
                    files=files,
                    timeout=15 
                )

                if response.status_code == 201:
                    print(f"Successfully synced detection ID: {detection_id}")
                    offline_storage.mark_as_synced(detection_id)
                else:
                    print(f"Failed to sync detection ID: {detection_id}. Status: {response.status_code}, Response: {response.text}")

        except FileNotFoundError:
            print(f"Image file disappeared for ID {detection_id}. Marking as synced.")
            offline_storage.mark_as_synced(detection_id)
        except requests.exceptions.RequestException as e:
            print(f"Network error while syncing detection ID {detection_id}: {e}")
            break # Stop trying if network is down
        except Exception as e:
            print(f"An unexpected error occurred for ID {detection_id}: {e}")
            
# --- Schedule the sync ---
schedule.every(5).minutes.do(sync_detections_to_cloud)
# schedule.every(30).seconds.do(sync_detections_to_cloud) # For faster testing

print("Cloud sync service started. Will sync every 5 minutes.")
sync_detections_to_cloud() # Run once on startup

while True:
    schedule.run_pending()
    time.sleep(1)