# 🍏 Week 02: Shape Analysis Lab Using Digital Image Processing
**– Circularity & Sphericity Computation with OpenCV, and GitHub Submission Guide –**

---

## 1. Geometric Shape Indices: Definition & Differences Between Circularity and Sphericity

Academically, "circularity" and "sphericity" are sometimes used interchangeably, but they serve different measurement purposes from a geometric standpoint.

### 1-1. Circularity
- **Definition**: Also known as the "Form Factor" or "Isoperimetric Quotient"
- **Purpose**: Evaluate how closely the overall shape of an object resembles a perfect circle
- **Formula**: `Circularity = (4 × π × Area) / Perimeter²`
- **Characteristics**:
  - A perfect circle yields a maximum value of 1.0
  - Values approach 0 as the shape becomes more distorted or the boundary becomes more complex
  - Highly sensitive to contour noise and surface roughness, since it depends on perimeter length

### 1-2. Sphericity & Roundness
- **Wadell's Sphericity**: 
  - Ratio of the surface area of a sphere with the same volume as the particle to the actual surface area
  - In 2D projections, it is indirectly estimated using the **area-to-circumscribed-circle-area ratio**, or the aspect ratio of the object's rotated bounding box
- **Roundness**:
  - Measures edge smoothness (mean radius of curvature / maximum inscribed circle radius)
  - Quantifies edge erosion independently of particle elongation

### [Summary Table]
| Index | Formula / Key Parameters | Measurement Target | Sensitivity |
| --- | --- | --- | --- |
| **Circularity** | `(4π × Area) / Perimeter²` | Overall proximity to a circle | Noise, shape irregularity |
| **Sphericity** | Geometric Mean Diameter / L, etc. | Surface area / volume ratio (3D proximity) | Elongation |
| **Roundness** | Edge curvature radius, etc. | Edge smoothness | Curvature, abrasion |

---

## 2. Step-by-Step Shape Analysis Algorithm via Digital Image Processing

### Step 1: Image Acquisition & Grayscale Conversion
- Reduces computational load by converting BGR (RGB) channels to a single-channel grayscale image for 1D operations

### Step 2: Noise Removal (Gaussian Blur)
- Smooths out specular reflections and surface texture noise from the apple surface
- Prevents perimeter over-estimation caused by noise, which would distort circularity calculations

### Step 3: Binarization (Otsu's Thresholding)
- Separates the foreground (apple) from the background
- Automatically determines the optimal threshold via histogram analysis

### Step 4: Contour Detection & Filtering
- Detects outer boundary coordinate arrays using `cv2.findContours`
- Filters out small noise objects based on area (`cv2.contourArea`)

### Step 5: Geometric Moment-Based Feature Extraction
- Extracts Area and Perimeter (`cv2.arcLength`)
- Can apply calibration markers (Ruler) for real-world mm conversion (PPM: Pixels Per Metric)

---

## 3. OpenCV Python Algorithm: Split Tutorial

This lab is organized into **3 separate Python files** so students can execute each step sequentially and visually understand the progressive transformations.

### 📝 [Required] Lab Environment Setup & Code Execution Instructions
1. **Install Packages**: Open your command prompt (cmd) or VS Code terminal and install the required libraries:
   ```bash
   pip install opencv-python numpy
   ```
2. **Create or Open Code Files**: Open each of the files described in Sections 3-1, 3-2, and 3-3 below in your editor. (The image file [`apple_side_A.png`](apple_side_A.png) must be in the same directory.)
3. **Run Scripts Sequentially**: Enter the following commands one by one in your terminal to observe how the image processing results change at each stage. Press **any key (e.g., Enter)** to close each display window and proceed.
   ```bash
   python step1_preprocess.py
   python step2_contour.py
   python step3_shape_analysis.py
   ```

---

### 3-1. `step1_preprocess.py`: Image Loading & Preprocessing
Converts the complex color image to grayscale and applies blur to suppress fine noise, preparing it for binarization and contour detection.

```python
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
```

### 3-2. [`step2_contour.py`](step2_contour.py): Binarization & Apple Contour Detection
Separates the apple from the background (Otsu's method) and extracts the outer boundary (contour) coordinate array from the white region.

```python
import cv2
import numpy as np

# (Continuing from previous step: loading and preprocessing assumed)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# 3. Binarization (white background → use INV option + Otsu auto-threshold)
_, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 4. Contour extraction
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 5. Contour visualization
for cnt in contours:
    area = cv2.contourArea(cnt)
    
    # [Important] Filter out small noise contours
    if area < 500:
        continue
    
    # Draw apple contour in green (0, 255, 0), thickness 2
    cv2.drawContours(original_display, [cnt], -1, (0, 255, 0), 2)

cv2.imshow("Step 2: Threshold & Contour", original_display)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### 3-3. [`step3_shape_analysis.py`](step3_shape_analysis.py): Final Shape Index Computation (Circularity & Sphericity)
Using the extracted contours, compute area and perimeter to derive circularity, and use the bounding box dimensions to mathematically estimate sphericity, then overlay the results on the image.

```python
import cv2
import numpy as np
import math

# (Continuing from steps 1-2: preprocessing and contour extraction assumed)
# ... [contours extracted up to this point] ...

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 500:
        continue
        
    perimeter = cv2.arcLength(cnt, True)
    if perimeter == 0:
        continue
        
    # 6. Shape index calculation
    # A. Circularity (ratio of perimeter to area)
    circularity = (4 * math.pi * area) / (perimeter ** 2)
    
    # B. Sphericity estimation via Bounding Box dimensions
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int32(box)  # Convert coordinates to integers for display
    
    dim1, dim2 = rect[1]
    pixel_L = max(dim1, dim2)
    pixel_W = min(dim1, dim2)
    
    # (Lab assumption: top-view pixel height T pre-measured as 304.1)
    pixel_T = 304.1
    GMD = (pixel_L * pixel_W * pixel_T) ** (1/3)
    sphericity = (GMD / pixel_L) * 100
    
    # 7. Visualization
    # Draw target apple contour (green) and bounding box (blue)
    cv2.drawContours(original_display, [cnt], -1, (0, 255, 0), 2)
    cv2.drawContours(original_display, [box], 0, (255, 0, 0), 2)
    
    # Compute geometric centroid using OpenCV moments
    M = cv2.moments(cnt)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
        
        # Display results near the centroid
        cv2.putText(original_display, f"Circularity: {circularity:.3f}", (cx - 60, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv2.putText(original_display, f"Sphericity: {sphericity:.1f}%", (cx - 60, cy + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

# 8. Final result GUI output
cv2.imshow("Step 3: Final Shape Analysis", original_display)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

### [Lab Discussion Point: Digital Grid Limitation (Aliasing)]
- Due to the nature of digital images, curved boundaries on diagonals are represented as stair-step grids
- This "staircase effect (aliasing)" always causes the measured perimeter to be longer than the actual perimeter
- Even for a perfectly spherical object, the computed circularity may be approximately `0.85 – 0.9` rather than `1.0` — students should reflect on why this occurs

---

## 4. Version Control & GitHub Submission Guide

*This course requires students to accumulate weekly assignments in a single master repository.*  
*For detailed instructions on initial GitHub setup and assignment submission (push), please refer to the **[Integrated Lab Submission Guide](../README.md)** in the top-level directory.*
