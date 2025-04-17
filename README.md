
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

##What the pipeline does:

<img width="681" alt="Screenshot 2025-04-17 at 8 09 59 PM" src="https://github.com/user-attachments/assets/fc3d120d-de0f-4aa2-9d3a-840993b5c9bc" />
<img width="662" alt="Screenshot 2025-04-17 at 8 09 50 PM" src="https://github.com/user-attachments/assets/010ae711-d0fc-4005-8f1f-e32a1906edae" />
<img width="538" alt="Screenshot 2025-04-17 at 8 09 32 PM" src="https://github.com/user-attachments/assets/5d62abdf-9e75-4742-90e7-d8cf13ac0725" />


