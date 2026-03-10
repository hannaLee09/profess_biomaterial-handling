"""
avocado_profile.py — Automatic Profile Extraction from Avocado Reference Image
===============================================================================
Uses OpenCV to detect the contour from avocado_front_view.png and extract
the lengthwise radius profile data.

Dependencies: pip install opencv-python numpy scipy
"""
import cv2
import numpy as np
import os


# Avocado total length from textbook Example 3-3 [cm]
AVOCADO_LENGTH_CM = 10.85


def _imread_unicode(filepath):
    """
    Load image from paths containing Unicode characters (e.g., Korean).
    cv2.imread() on Windows does not support non-ASCII paths,
    so we use numpy + cv2.imdecode as a workaround.
    """
    try:
        with open(filepath, 'rb') as f:
            buf = np.frombuffer(f.read(), dtype=np.uint8)
        img = cv2.imdecode(buf, cv2.IMREAD_COLOR)
        return img
    except Exception:
        return None


def extract_profile(image_path=None, n_dense=200):
    """
    Load the avocado image and extract contour-based profile data.

    Parameters
    ----------
    image_path : str, optional
        Path to image file. If None, auto-searches images/avocado_front_view.png
    n_dense : int
        Number of dense profile samples (default 200)

    Returns
    -------
    dict
        x_points, r_points   : Points for spline fitting (~15, reinforced at ends)
        x_textbook, r_textbook : Textbook measurement points (6)
        x_dense, r_dense     : Dense profile (n_dense points)
        image                 : Original image (BGR)
        contour               : Detected avocado contour
        scale                 : Pixel-to-cm conversion factor
        from_image            : Whether image processing succeeded
    """
    if image_path is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(script_dir, 'images', 'avocado_front_view.png')

    image = _imread_unicode(image_path)
    if image is None:
        print(f"[WARNING] Image not found: {image_path}")
        print("[FALLBACK] Using textbook Example 3-3 data.")
        return _fallback_data()

    print(f"[INFO] Image loaded: {image_path}")
    print(f"       Size: {image.shape[1]} x {image.shape[0]} px")

    try:
        result = _process_image(image, n_dense)
        print(f"[INFO] Profile extraction successful -- Length: {result['x_points'][-1]:.2f} cm, "
              f"Max radius: {result['r_points'].max():.3f} cm")
        return result
    except Exception as e:
        print(f"[WARNING] Image processing failed ({e})")
        print("[FALLBACK] Using textbook Example 3-3 data.")
        return _fallback_data()


def _process_image(image, n_dense):
    """OpenCV-based image processing pipeline."""
    h_img, w_img = image.shape[:2]

    # 1) Grayscale + Gaussian blur
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    # 2) Otsu binarization (bright background → invert)
    _, binary = cv2.threshold(blurred, 0, 255,
                              cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 3) Morphological operations: noise removal & object connection
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9))
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=3)
    binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=2)

    # 4) Contour detection
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_NONE)

    # Filter by area (> 1% of total image)
    min_area = h_img * w_img * 0.01
    valid = [c for c in contours if cv2.contourArea(c) > min_area]
    if not valid:
        raise ValueError("No valid contours found")

    # Largest contour = avocado
    avocado = max(valid, key=cv2.contourArea)
    bx, by, bw, bh = cv2.boundingRect(avocado)
    pts = avocado.reshape(-1, 2)

    # 5) Orientation detection & scale calculation
    if bh >= bw:
        # Vertical — length axis along Y
        length_px = bh
        scale = AVOCADO_LENGTH_CM / length_px
        positions = np.linspace(by, by + bh, n_dense)
        radii_px = _extract_widths(pts, positions, axis='y',
                                   tol=max(3, bh * 0.015))
        x_cm = (positions - by) * scale
    else:
        # Horizontal — length axis along X
        length_px = bw
        scale = AVOCADO_LENGTH_CM / length_px
        positions = np.linspace(bx, bx + bw, n_dense)
        radii_px = _extract_widths(pts, positions, axis='x',
                                   tol=max(3, bw * 0.015))
        x_cm = (positions - bx) * scale

    r_cm = np.array(radii_px) * scale

    # 6) Smoothing + correction
    from scipy.ndimage import uniform_filter1d
    r_cm = uniform_filter1d(r_cm, size=9)
    r_cm = np.maximum(r_cm, 0)
    r_cm[0] = 0
    r_cm[-1] = 0

    # 7) Sample 6 key points matching textbook measurement positions
    textbook_ratios = np.array([0, 1.0, 5.0, 6.5, 8.0, 10.85]) / AVOCADO_LENGTH_CM
    textbook_x = textbook_ratios * x_cm[-1]
    textbook_r = np.interp(textbook_x, x_cm, r_cm)
    textbook_r[0] = 0
    textbook_r[-1] = 0

    # 8) Points for spline fitting: evenly spaced + reinforced near ends
    #    Using only 6 points causes spline overshoot due to wide spacing,
    #    so we provide sufficient points for accurate interpolation.
    n_spline = 15
    spline_x = np.linspace(0, x_cm[-1], n_spline)
    # Add extra points near endpoints (tapering reinforcement)
    extra_near_start = np.array([x_cm[-1] * 0.02, x_cm[-1] * 0.05])
    extra_near_end = np.array([x_cm[-1] * 0.95, x_cm[-1] * 0.98])
    spline_x = np.unique(np.sort(np.concatenate([spline_x, extra_near_start, extra_near_end])))
    spline_r = np.interp(spline_x, x_cm, r_cm)
    spline_r[0] = 0
    spline_r[-1] = 0

    return {
        'x_points': spline_x,
        'r_points': spline_r,
        'x_textbook': textbook_x,
        'r_textbook': textbook_r,
        'x_dense': x_cm,
        'r_dense': r_cm,
        'image': image,
        'contour': avocado,
        'binary': binary,
        'scale': scale,
        'bbox': (bx, by, bw, bh),
        'from_image': True,
    }


def _extract_widths(pts, positions, axis, tol):
    """Extract half-width (radius) at each position from contour points."""
    radii = []
    for pos in positions:
        if axis == 'y':
            mask = np.abs(pts[:, 1] - pos) < tol
            nearby = pts[mask]
            if len(nearby) >= 2:
                radii.append((nearby[:, 0].max() - nearby[:, 0].min()) / 2.0)
            else:
                radii.append(0)
        else:
            mask = np.abs(pts[:, 0] - pos) < tol
            nearby = pts[mask]
            if len(nearby) >= 2:
                radii.append((nearby[:, 1].max() - nearby[:, 1].min()) / 2.0)
            else:
                radii.append(0)
    return radii


def _fallback_data():
    """Textbook Example 3-3 hardcoded data (when image is unavailable)."""
    x = np.array([0, 1.0, 5.0, 6.5, 8.0, 10.85])
    r = np.array([0, 1.47, 3.185, 3.38, 3.04, 0])
    return {
        'x_points': x,
        'r_points': r,
        'x_textbook': x.copy(),
        'r_textbook': r.copy(),
        'x_dense': None,
        'r_dense': None,
        'image': None,
        'contour': None,
        'binary': None,
        'scale': None,
        'bbox': None,
        'from_image': False,
    }


# === Test when run directly ===
if __name__ == '__main__':
    data = extract_profile()
    print("\n=== Extracted Measurement Points ===")
    print(f"{'Position x [cm]':>16} | {'Radius r [cm]':>14}")
    print("-" * 34)
    for x, r in zip(data['x_points'], data['r_points']):
        print(f"{x:>16.3f} | {r:>14.3f}")
    print(f"\nImage-based: {'Yes' if data['from_image'] else 'No (textbook data)'}")
