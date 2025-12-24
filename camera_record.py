import cv2
import os

# --- USER SETTINGS ---
SAVE_PATH = r"E:\Madhav\CDM\Dataset_camera"     # <--- Change this path
CAMERA_INDEX = 0                        # <--- Set this to the index found in step 1
# ---------------------

if not os.path.exists(SAVE_PATH):
    os.makedirs(SAVE_PATH)

cap = cv2.VideoCapture(CAMERA_INDEX, cv2.CAP_DSHOW)

# Setup Video Writer
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
out = None
is_recording = False

print(f"Camera opened. Saving videos to: {SAVE_PATH}")
print("Controls: 'c' = Start Recording, 'q' = Quit")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # If recording, write the frame to the file
    if is_recording:
        out.write(frame)
        # Draw a red circle and text on the PREVIEW window so you know it's recording
        cv2.circle(frame, (30, 30), 10, (0, 0, 255), -1)
        cv2.putText(frame, "REC", (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Show the window (This allows you to see what the camera sees)
    cv2.imshow("Video Record Mode", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        if not is_recording:
            # START Recording
            video_name = os.path.join(SAVE_PATH, "cdm_test_video.mp4")
            out = cv2.VideoWriter(video_name, fourcc, 30.0, (frame_width, frame_height))
            is_recording = True
            print(f"Recording STARTED: {video_name}")
        else:
            # STOP Recording
            is_recording = False
            out.release()
            print("Recording STOPPED. Saved.")
            
            # Visual feedback on screen
            cv2.putText(frame, "SAVED", (150, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 3)
            cv2.imshow("Video Record Mode", frame)
            cv2.waitKey(500)

    elif key == ord('q'):
        break

if out:
    out.release()
cap.release()
cv2.destroyAllWindows()