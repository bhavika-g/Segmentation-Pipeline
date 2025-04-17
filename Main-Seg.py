import cv2
import numpy as np
import os
import argparse

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def contrast_enhancement(input_dir, output_dir):
    ensure_dir(output_dir)
    for file in sorted(os.listdir(input_dir)):
        if file.endswith('.tiff'):
            image = cv2.imread(os.path.join(input_dir, file), cv2.IMREAD_UNCHANGED)
            clahe = cv2.createCLAHE(clipLimit=35, tileGridSize=(1, 1))
            enhanced = clahe.apply(image)
            _, thresholded = cv2.threshold(enhanced, 48143, 64680, cv2.THRESH_BINARY)
            thresholded = (thresholded / 256).astype('uint8')
            cv2.imwrite(os.path.join(output_dir, f"{file}_enhanced_thresh.tiff"), thresholded)

def contour_convex_hull(main_dir):
    input_dir = os.path.join(main_dir, "ce_thresholded")
    contour_dir = os.path.join(main_dir, "contour")
    hull_dir = os.path.join(main_dir, "convex_hull")
    ensure_dir(contour_dir)
    ensure_dir(hull_dir)

    for file in sorted(os.listdir(input_dir)):
        if file.endswith('.tiff'):
            image = cv2.imread(os.path.join(input_dir, file), cv2.IMREAD_UNCHANGED)
            contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                continue
            largest = max(contours, key=cv2.contourArea)

            contour_image = np.zeros_like(image)
            cv2.drawContours(contour_image, [largest], -1, (65535, 65535), -1)
            contour_image = cv2.erode(contour_image, np.ones((5, 5), np.uint8), iterations=1)
            cv2.imwrite(os.path.join(contour_dir, f"{file}_contour.tiff"), contour_image)

            hull_image = np.zeros_like(image)
            cv2.drawContours(hull_image, [cv2.convexHull(largest)], -1, (65535, 65535), -1)
            cv2.imwrite(os.path.join(hull_dir, f"{file}_convex_hull.tiff"), hull_image)

def extract_OL(main_dir):
    input_dir = main_dir
    mask_dir = os.path.join(main_dir, "convex_hull")
    output_dir = os.path.join(main_dir, "OL_outline")
    ensure_dir(output_dir)

    images = sorted([f for f in os.listdir(input_dir) if f.endswith('.tiff')])
    masks = sorted([f for f in os.listdir(mask_dir) if f.endswith('.tiff')])

    for image_file, mask_file in zip(images, masks):
        image = cv2.imread(os.path.join(input_dir, image_file), cv2.IMREAD_UNCHANGED)
        mask = cv2.imread(os.path.join(mask_dir, mask_file), cv2.IMREAD_UNCHANGED)
        out = image.copy()
        out[mask == 0] = 0
        cv2.imwrite(os.path.join(output_dir, f"{image_file}_outline.tiff"), out)

def contrast_enhancement_2(main_dir):
    input_dir = os.path.join(main_dir, "OL_outline")
    output_dir = os.path.join(main_dir, "contrast_enhanced_2")
    ensure_dir(output_dir)

    for file in sorted(os.listdir(input_dir)):
        if file.endswith('.tiff'):
            image = cv2.imread(os.path.join(input_dir, file), cv2.IMREAD_UNCHANGED)
            image = cv2.convertScaleAbs(image, alpha=(255.0 / 65535.0))
            clahe = cv2.createCLAHE(clipLimit=35, tileGridSize=(1, 1))
            image = clahe.apply(image)
            blur = cv2.GaussianBlur(image, (21, 21), 0)
            blur = cv2.fastNlMeansDenoising(blur, None, h=10)
            thresholded = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                                cv2.THRESH_BINARY, 115, 0)
            cv2.imwrite(os.path.join(output_dir, f"{file}_contrast.tiff"), thresholded)

def cortex_subtract(main_dir):
    input_dir = os.path.join(main_dir, "contrast_enhanced_2")
    output_dir = os.path.join(main_dir, "cortex_removed")
    ensure_dir(output_dir)

    for file in sorted(os.listdir(input_dir)):
        if file.endswith('.tiff'):
            image = cv2.imread(os.path.join(input_dir, file), cv2.IMREAD_UNCHANGED)
            _, labels, stats, _ = cv2.connectedComponentsWithStats(image)
            max_label = 1 + np.argmax(stats[1:, cv2.CC_STAT_AREA])
            mask = np.where(labels == max_label, 0, image)
            cv2.imwrite(os.path.join(output_dir, f"{file}.tiff"), mask)

# Entry point
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run synapse preprocessing pipeline.")
    parser.add_argument("--input_dir", required=True, help="Path to input directory with raw .tiff files")
    args = parser.parse_args()

    main_dir = args.input_dir

    print(f"Running pipeline on: {main_dir}")

    contrast_enhancement(main_dir, os.path.join(main_dir, "ce_thresholded"))
    contour_convex_hull(main_dir)
    extract_OL(main_dir)
    contrast_enhancement_2(main_dir)
    cortex_subtract(main_dir)

    print("✅ Processing complete.")
