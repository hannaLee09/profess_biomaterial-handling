import cv2
import numpy as np

# 1. Load image (using imdecode for cross-platform path support)
image_path = 'apple_side_A.png'
img_array = np.fromfile(image_path, np.uint8)
img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

if img is None:
    print("Error: Image file not found.")
    exit()

original_display = img.copy()

# 2. Preprocessing (Grayscale conversion & Gaussian Blur)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Display intermediate result (press any key to close window)
cv2.imshow("Step 1: Grayscale & Blurred", blurred)
cv2.waitKey(0)
cv2.destroyAllWindows()
