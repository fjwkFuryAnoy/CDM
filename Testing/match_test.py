import cv2
import numpy as np
import os

# --- CONFIGURATION ---
TEST_IMAGE_PATH = "test_images/SP_10.jpg" # The card you want to identify
TEMPLATE_FOLDER = "templates"
# ---------------------

# 1. Load Templates
templates = {}
for filename in os.listdir(TEMPLATE_FOLDER):
    if filename.endswith(".jpg"):
        # Load in grayscale (0 flag)
        path = os.path.join(TEMPLATE_FOLDER, filename)
        templates[filename.split('.')[0]] = cv2.imread(path, 0)

if not templates:
    print("Error: No templates found! Run Step 1 first.")
    exit()

# 2. Load and Preprocess Test Image
original_img = cv2.imread(TEST_IMAGE_PATH)
if original_img is None:
    print(f"Error: Could not load {TEST_IMAGE_PATH}")
    exit()

# Convert to grayscale
gray_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)

print(f"Testing image: {TEST_IMAGE_PATH}")
print("-" * 30)

# 3. Run Template Matching
best_match_name = "Unknown"
best_match_score = 0
best_location = None

for suit_name, template_img in templates.items():
    # cv2.matchTemplate scans the template over the image
    # TM_CCOEFF_NORMED is robust: 1 = perfect match, -1 = mismatch
    result = cv2.matchTemplate(gray_img, template_img, cv2.TM_CCOEFF_NORMED)
    
    # Get the best score for this specific suit
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    
    print(f"Checking {suit_name}... Score: {max_val:.2f}")
    
    # If this suit has a higher score than the previous best, store it
    if max_val > best_match_score:
        best_match_score = max_val
        best_match_name = suit_name
        best_location = max_loc
        best_template_size = template_img.shape[::-1]

# 4. Show Result
print("-" * 30)
if best_match_score > 0.7: # Threshold (70% confidence)
    print(f"RESULT: Identified as {best_match_name} ({best_match_score:.2f})")
    
    # Draw a box around the matched area
    top_left = best_location
    w, h = best_template_size
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(original_img, top_left, bottom_right, (0, 255, 0), 3)
    cv2.putText(original_img, f"{best_match_name}", (top_left[0], top_left[1]-10), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
else:
    print("RESULT: No Match Found (Score too low)")

cv2.imshow("Identification Result", original_img)
cv2.waitKey(0)
cv2.destroyAllWindows()