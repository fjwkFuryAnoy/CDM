import cv2
import os

# --- CONFIGURATION ---
# Image to load (choose one of your uploaded files)
SOURCE_IMAGE_PATH = "test_images\HE_A.jpg"
# Name to save the template as (e.g., "Spade", "Heart", "Diamond", "Club")
SUIT_NAME = "HEART"
SAVE_FOLDER = "templates"
# ---------------------

if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)

# 1. Load the image
img = cv2.imread(SOURCE_IMAGE_PATH)
if img is None:
    print(f"Error: Could not find {SOURCE_IMAGE_PATH}")
    exit()

print("INSTRUCTIONS:")
print("1. Click and drag to draw a box around the SUIT symbol (the Spade).")
print("2. Press ENTER to save the crop.")
print("3. Press 'c' to cancel.")

# 2. Select ROI (Region of Interest)
# This opens a window where you can draw a box.
roi = cv2.selectROI("Select Suit", img, showCrosshair=True, fromCenter=False)
cv2.destroyWindow("Select Suit")

# 3. Save the crop
if roi[2] > 0 and roi[3] > 0:  # Check if a valid box was drawn
    x, y, w, h = int(roi[0]), int(roi[1]), int(roi[2]), int(roi[3])
    suit_crop = img[y:y+h, x:x+w]
    
    # Save as grayscale (Standard for template matching)
    suit_gray = cv2.cvtColor(suit_crop, cv2.COLOR_BGR2GRAY)
    
    save_path = os.path.join(SAVE_FOLDER, f"{SUIT_NAME}.jpg")
    cv2.imwrite(save_path, suit_gray)
    print(f"Success! Saved template to: {save_path}")
    
    # Show what we saved
    cv2.imshow("Saved Template", suit_gray)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Selection canceled.")