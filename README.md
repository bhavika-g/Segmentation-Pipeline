
This repository contains a modular, CLI-based pipeline for performing contrast enhancement, contour detection, convex hull extraction, and cortex subtraction on microscopy `.tiff` images for processing microCT scans of the optic lobe of the cuttlefish. 

The pipeline is designed to run sequentially from a **single entry point**, requiring only the input directory containing raw `.tiff` files. All intermediate and final outputs are saved in subdirectories created automatically within that folder.

---

## 📂 Pipeline Overview

```text
Input Directory/
├── *.tiff                         # Raw microscopy images
├── ce_thresholded/               # CLAHE-enhanced + thresholded images
├── contour/                      # Largest contour masks
├── convex_hull/                  # Convex hull of main structure
├── OL_outline/                   # OL-masked raw input
├── contrast_enhanced_2/          # Denoised + adaptively thresholded output
└── cortex_removed/               # Final cortex-subtracted image

```

## Steps to use the pipeline

### 1. Create a virtual environment
``` bash
python3 -m venv sptool-env
source sptool-env/bin/activate   # On Windows: sptool-env\Scripts\activate

```

### 2. Install dependencies

``` bash
pip install -r requirements.txt
 ```

### 3. Run the pipeline 

``` bash

python Main-Seg.py --input_dir /path/to/your/image_folder

```

## Guidelines 

1. The input folder should contain a series of 2D .tiff stacks forming a 3D volume. The names of the files should be numbered according to the slice number (For example, 0001.tiff, 0002.tiff....)

2. The repository contains some demo data in the 'Examples' folder. 

