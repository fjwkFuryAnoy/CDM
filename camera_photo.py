import cv2
import os

# --- USER SETTINGS ---
SAVE_PATH = r"E:\Madhav\CDM\Dataset_camera"  # <--- Change this path
CAMERA_INDEX = 0                        # <--- Set this to the index found in step 1
# ---------------------

if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

cap = cv2.VideoCapture(CAMERA_INDEX)
count = 0

# --- ADD THIS CHECK ---
if not cap.isOpened():
    print(f"ERROR: Could not open camera at index {CAMERA_INDEX}.")
    print("Try changing CAMERA_INDEX to 0 or 2.")
    exit()
# ----------------------

print(f"Camera opened. Saving photos to: {SAVE_PATH}")
print("Controls: 'c' = Capture, 'q' = Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Show the live feed in a window
    cv2.imshow("Photo Mode - Press 'c' to Capture", frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('c'):
        # Save the image
        filename = f"image_{count}.jpg"
        full_path = os.path.join(SAVE_PATH, filename)
        cv2.imwrite(full_path, frame)
        
        print(f"Captured: {filename}")
        count += 1
        
        # Visual feedback: Flash "Saved" on the screen for 200ms
        cv2.putText(frame, "SAVED!", (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
        cv2.imshow("Photo Mode - Press 'c' to Capture", frame)
        cv2.waitKey(200) 

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()