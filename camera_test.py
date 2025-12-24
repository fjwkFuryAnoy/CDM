import cv2

def test_camera_feed():
    # Try indices 0, 1, 2 to find your USB camera
    for index in range(3):
        print(f"Testing Camera Index: {index}...")
        cap = cv2.VideoCapture(index, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print(f"Index {index}: No camera found.")
            cap.release()
            continue

        print(f"Index {index}: Success! Opening feed...")
        print("Press 'q' if this is the correct camera to STOP.")
        print("Press any other key to try the NEXT camera index.")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            # Add text to the video feed so you know which index this is
            cv2.putText(frame, f"Camera Index: {index}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            cv2.imshow(f"Test Feed - Index {index}", frame)
            
            # Wait for user input
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                print(f"Selected Camera Index: {index}")
                return # Stop script, we found it
            elif key != 255: # If any other key is pressed
                break # Break loop to try next index
        
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    test_camera_feed()