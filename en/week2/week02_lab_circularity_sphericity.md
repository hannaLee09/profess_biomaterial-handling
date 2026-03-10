# 🍏 Week 02: Shape Analysis Lab Using Digital Image Processing
**– Circularity & Sphericity Computation with [OpenCV](https://docs.opencv.org/4.x/), and GitHub Submission Guide –**

> 📂 **Navigate**: [← Main README](../README.md) · [Week 03: Volume & Surface Area →](../week3/week03_lab_volume_surface_area.md) · [📝 Quiz Bank](../QUIZ_BANK.md)

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
- **[Wadell's Sphericity](https://en.wikipedia.org/wiki/Sphericity)**: 
  - Ratio of the surface area of a sphere with the same [volume](../week3/week03_lab_volume_surface_area.md) as the particle to the actual [surface area](../week3/week03_lab_volume_surface_area.md)
  - In 2D projections, it is indirectly estimated using the **area-to-circumscribed-circle-area ratio**, or the aspect ratio of the object's rotated bounding box
- **[Roundness](https://en.wikipedia.org/wiki/Roundness)**:
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

### Step 3: Binarization ([Otsu's Thresholding](https://en.wikipedia.org/wiki/Otsu%27s_method))
- Separates the foreground (apple) from the background
- Automatically determines the optimal threshold via histogram analysis

### Step 4: Contour Detection & Filtering
- Detects outer boundary coordinate arrays using [`cv2.findContours`](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#gadf1ad6a0b82947fa1fe3c3d497f260e0)
- Filters out small noise objects based on area ([`cv2.contourArea`](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#ga2c759ed9f497d4a618048a2f56dc97f1))

### Step 5: Geometric Moment-Based Feature Extraction
- Extracts Area and Perimeter ([`cv2.arcLength`](https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#ga8d26f1c594aab4d24a4c6e3ca0ecfb32))
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

## 4. 💡 Advanced Discussion Topics

### Discussion 1: Impact of Digital Aliasing on Shape Analysis

**Background**: When measuring the circularity of a nearly perfect sphere-like apple using OpenCV, the result is approximately `0.85–0.9` rather than the theoretical `1.0`. This is due to aliasing — the pixel grid of digital images represents curved boundaries as stair-step patterns, causing the perimeter to be measured longer than its actual value.

> **Discussion Prompt**: What software-based approaches could correct this perimeter over-estimation caused by aliasing? (e.g., subpixel contour detection, adjusting Gaussian blur intensity, resolution-dependent circularity convergence experiments, etc.)

### Discussion 2: Industrial Applications of Circularity & Sphericity — Automated Agricultural Produce Sorting

**Background**: In automated sorting lines for agricultural products, cameras must distinguish defective items with non-standard shapes in real-time using only 2D images. Circularity measures how closely a 2D projected shape resembles a circle, while sphericity measures 3D proximity to a sphere — but obtaining 3D information from a single camera is inherently challenging.

> **Discussion Prompt**: To estimate 3D sphericity from only 2D images of an apple moving on a conveyor belt (one front view, one side view), what assumptions and algorithms are needed, and what are their limitations? Include in your discussion the significance of the pre-measured `pixel_T` (thickness) value used in this lab.

### Discussion 3: Impact of Thresholding Method Selection on Shape Indices

**Background**: This lab uses Otsu's automatic thresholding to separate the apple from the background. However, under non-uniform lighting conditions or when background colors are similar to the apple, binarization results may vary, distorting the contour and directly introducing errors into circularity and sphericity calculations.

> **Discussion Prompt**: Besides Otsu's binarization, alternative techniques such as Adaptive Thresholding and HSV color space segmentation exist. What are the advantages and disadvantages of each for agricultural image analysis, and under what circumstances is each approach optimal?

---

## 5. 📝 Quiz Questions

### Q1. [Theory] Definition of Circularity
Which formula correctly represents **Circularity** as used in OpenCV-based image analysis?

| Option | Formula |
| --- | --- |
| A | `Perimeter / Area` |
| B | `Area / Perimeter²` |
| **C** | **`(4 × π × Area) / Perimeter²`** |
| D | `(Circumscribed circle area) / (Actual area)` |

<details>
<summary>View Answer & Explanation</summary>

**Answer: C**  
Circularity (Form Factor) is defined as `Circularity = (4πA) / P²`. A perfect circle yields 1.0, and more complex shapes approach 0. Since perimeter² is in the denominator, this metric is sensitive to contour noise.
</details>

### Q2. [Lab - Python] Role of Otsu's Thresholding
Why is the `cv2.THRESH_OTSU` flag used in the `cv2.threshold()` function?

| Option | Content |
| --- | --- |
| A | To automatically adjust image resolution |
| **B** | **To automatically determine the optimal threshold for separating foreground and background via histogram analysis** |
| C | To convert a color image to grayscale |
| D | To calculate contour area |

<details>
<summary>View Answer & Explanation</summary>

**Answer: B**  
Otsu's method automatically finds the threshold that maximizes between-class variance in the image histogram, effectively separating background and foreground without requiring manual threshold specification.
</details>

### Q3. [Lab - Python] Meaning of Geometric Mean Diameter (GMD) in Sphericity Calculation
In this lab, sphericity is calculated using `GMD = (L × W × T)^(1/3)`. What does the Geometric Mean Diameter (GMD) represent?

<details>
<summary>View Answer & Explanation</summary>

**Answer: The geometric mean of three-dimensional measurements (Length L, Width W, Thickness T), representing the diameter of a sphere that would equivalently represent the irregular shape.**  
The ratio of GMD to the maximum dimension (L) gives sphericity — values closer to 100% indicate a more sphere-like shape. Apples typically have ~90% sphericity, while grains range from 50–60%.
</details>

### Q4. [Theory] Purpose of Gaussian Blur Preprocessing
What is the most important reason for applying Gaussian Blur immediately after grayscale conversion in the image analysis pipeline?

| Option | Content |
| --- | --- |
| A | To reduce the number of color channels |
| B | To enhance image contrast |
| **C** | **To smooth surface texture and lighting noise, preventing perimeter over-estimation (circularity distortion) during binarization and contour extraction** |
| D | To accurately measure object area |

<details>
<summary>View Answer & Explanation</summary>

**Answer: C**  
Fine spots, textures, and specular reflections on the apple surface create unnecessary contour irregularities after binarization, causing perimeter over-measurement. Since Perimeter² is in the denominator of the circularity formula, noise-induced perimeter increase distorts circularity below its actual value. Gaussian Blur removes this high-frequency noise beforehand.
</details>

---

## 6. Version Control & GitHub Submission Guide

*This course requires students to accumulate weekly assignments in a single master repository.*  
*For detailed instructions on initial GitHub setup and assignment submission (push), please refer to the **[Integrated Lab Submission Guide](../README.md)** in the top-level directory.*

