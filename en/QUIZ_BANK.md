# 📚 Weekly Discussion Topics & Quiz Bank
> A consolidated reference of advanced discussion topics and quiz questions from the **Biomaterial Handling & Processing** lab course.  
> 📌 **[한국어 버전](../ko/QUIZ_BANK.md)**

---

## 📖 Table of Contents
- [Week 02: Circularity & Sphericity](#week-02-circularity--sphericity)
- [Week 03: Volume & Surface Area Estimation](#week-03-volume--surface-area-estimation)

---

# Week 02: Circularity & Sphericity
> 🔗 [View Detailed Lab Tutorial](week2/week02_lab_circularity_sphericity.md)

## 💡 Discussion Topics

### Discussion 1: Impact of Digital Aliasing on Shape Analysis

**Background**: When measuring circularity of a nearly spherical apple via OpenCV, the result is ~`0.85–0.9` instead of the theoretical `1.0`, due to aliasing — the pixel grid represents curved boundaries as stair-steps, causing perimeter over-measurement.

> **Prompt**: What software-based approaches could correct aliasing-induced perimeter over-estimation? (e.g., subpixel contour detection, Gaussian blur intensity adjustment, resolution-dependent circularity convergence experiments)

### Discussion 2: Industrial Applications — Automated Agricultural Produce Sorting

**Background**: Automated sorting lines must distinguish defective shapes in real-time using only 2D images. Circularity is a 2D metric while sphericity is 3D — but single cameras cannot directly capture 3D information.

> **Prompt**: To estimate 3D sphericity from only 2D images (front + side views) of an apple on a conveyor belt, what assumptions and algorithms are needed, and what are their limitations?

### Discussion 3: Impact of Thresholding Method on Shape Indices

**Background**: Otsu's auto-thresholding is used, but non-uniform lighting or similar background colors can distort contours and introduce errors in circularity/sphericity.

> **Prompt**: What are the pros and cons of Adaptive Thresholding, HSV color space segmentation, and other alternatives for agricultural image analysis?

---

## 📝 Quiz Questions

### Q1. [Theory] Definition of Circularity
Which formula correctly represents **Circularity** in OpenCV-based image analysis?

| Option | Formula |
| --- | --- |
| A | `Perimeter / Area` |
| B | `Area / Perimeter²` |
| **C** | **`(4 × π × Area) / Perimeter²`** |
| D | `(Circumscribed circle area) / (Actual area)` |

<details>
<summary>View Answer</summary>

**Answer: C** — Perfect circle yields 1.0; complex shapes approach 0. Sensitive to contour noise due to P² in denominator.
</details>

### Q2. [Lab] Role of Otsu's Thresholding
Why is `cv2.THRESH_OTSU` used in `cv2.threshold()`?

| Option | Content |
| --- | --- |
| A | Auto-adjust image resolution |
| **B** | **Auto-determine optimal threshold via histogram analysis** |
| C | Convert color to grayscale |
| D | Calculate contour area |

<details>
<summary>View Answer</summary>

**Answer: B** — Maximizes between-class variance to automatically separate foreground/background.
</details>

### Q3. [Lab] Meaning of Geometric Mean Diameter (GMD)
Sphericity uses `GMD = (L × W × T)^(1/3)`. What does GMD represent?

<details>
<summary>View Answer</summary>

**Answer**: Geometric mean of 3D dimensions (L, W, T) — the diameter of an equivalent sphere. GMD/L ratio = sphericity; closer to 100% = more spherical. Apples ~90%, grains 50–60%.
</details>

### Q4. [Theory] Purpose of Gaussian Blur
Why is Gaussian Blur applied immediately after grayscale conversion?

| Option | Content |
| --- | --- |
| A | Reduce color channels |
| B | Enhance contrast |
| **C** | **Smooth noise to prevent perimeter over-estimation (circularity distortion)** |
| D | Accurately measure area |

<details>
<summary>View Answer</summary>

**Answer: C** — Surface noise inflates perimeter, and since P² is in the circularity denominator, this distorts the value downward. Blur removes high-frequency noise.
</details>

---

# Week 03: Volume & Surface Area Estimation
> 🔗 [View Detailed Lab Tutorial](week3/week03_lab_volume_surface_area.md)

## 💡 Discussion Topics

### Discussion 1: Limitations of Geometric Simplification

**Background**: Manual 5-segment calculation yields ~8.03% surface area and ~4.33% volume errors. Python applies 100+ segment numerical integration.

> **Prompt**: Beyond increasing subdivisions (n), what are the fundamental **'asymmetry limitations'** of single-view 2D profile rotation integration, and how can 3D digital metrology address these?

### Discussion 2: Specific Surface Area & Processing Operations

**Background**: Wheat (1,316 m²/m³) dries significantly faster than soybeans (558 m²/m³) under identical conditions.

> **Prompt**: What engineering strategies should be adopted when designing cooling/ventilation systems for large-scale long-term storage silos, applying the physical properties of specific surface area?

### Discussion 3: Liquid Displacement vs. Air Pycnometer

**Background**: Low-moisture materials → water displacement (Archimedes); moisture-absorbing grains → air pycnometer (Boyle's Law).

> **Prompt**: What impact could **temperature changes** within the pycnometer chamber have on precision, and what cross-validation methods can improve reliability?

---

## 📝 Quiz Questions

### Q1. [Theory] Primary Error Source in Segmental Modeling
What is the **most significant cause** of error when applying segmental modeling?

| Option | Content |
| --- | --- |
| A | Internal moisture content differences |
| B | Numerical integration formula errors |
| **C** | **Geometric assumptions simplifying natural curvature into mathematical shapes** |
| D | Caliper quantization errors |

<details>
<summary>View Answer</summary>

**Answer: C** — Linearizing continuous curvature into truncated cones causes ~8.03% surface area and ~4.33% volume error.
</details>

### Q2. [Lab] Preprocessing Interpolation Technique
What technique converts discrete measurement points into a smooth function curve?

<details>
<summary>View Answer</summary>

**Answer: Cubic Spline Interpolation** — `scipy.interpolate.CubicSpline` converts discrete data into 100+ continuous curve points.
</details>

### Q3. [Lab] Numerical Integration Comparison
Which function provides higher precision than `trapezoid` by using **2nd-order parabolic approximation**?

<details>
<summary>View Answer</summary>

**Answer: Simpson's Rule (`scipy.integrate.simpson`)** — O(h⁴) accuracy via parabolic approximation, advantageous for curved surfaces.
</details>

### Q4. [Theory] Air Pycnometer Physical Law
What **fundamental physical law** does the air pycnometer apply?

<details>
<summary>View Answer</summary>

**Answer: Boyle's Law** — At constant temperature, pressure and volume are inversely proportional, enabling precise absolute volume calculation.
</details>

---

*This document is updated as new weeks are added.*
