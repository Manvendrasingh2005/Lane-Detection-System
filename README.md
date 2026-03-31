# Lane Detection System

## 1. Project Overview
This project is a Computer Vision-based Lane Detection System built using Python and OpenCV. It relies on fundamental image processing techniques, edge detection algorithms, and logical filtering to identify lane markings on roads and vividly overlay tracking lines in real-time. 

## 2. Technical Methodology
The analytical pipeline for processing a frame comprises the following distinct stages:
1. **Grayscale Conversion**: Reduces spatial complexity from 3 channels (RGB) to 1, facilitating gradient detection.
2. **Gaussian Blur**: Applies a `5x5` moving kernel convolution to organically smooth out high-frequency noise without losing firm road edges.
3. **Canny Edge Detection**: Employs rapid intensity gradient checking to isolate mathematical boundaries (`thresholds=50,150`).
4. **Region of Interest (ROI)**: Isolates the lower portion of the frame using an explicitly defined trapezoid to mask off external distractions (sky, roadside vegetation, adjacent cars).
5. **Hough Line Transform**: Uses `cv2.HoughLinesP` to algorithmically map scattered pixel points into continuous linear vectors.
6. **Slope/Intercept Averaging**: The script categorizes the resulting vectors into distinct "left" and "right" sets by looking at the slope (negative logic vs positive logic). It averages these linear coefficients and generates two definitive lines overlaying the vehicle's driving path.

## 3. Environment Setup & Execution

### Prerequisites
- Python 3.7+
- Explicitly: `opencv-python` and `numpy`

### Setup Instructions
1. Clone the repository and navigate into it:
   ```bash
   git clone https://github.com/Manvendrasingh2005/Lane-Detection-System.git
   cd Lane-Detection-System
   ```
2. Create and activate a Virtual Environment (Highly Recommended):
   - **Windows:** 
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **Linux/Mac:** 
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Execution (Command Line Usage)
The core script accepts structural arguments via `argparse`, making it completely adaptable to different test files and server environments.

**Option A: Running with UI Playback**
Suitable for local desktop environments where a GUI can render live popups.
```bash
python main.py --input test_video.mp4
```

**Option B: Running in Headless Mode (CLI Fully)**
Specifying an `--output` argument instructs the system to completely skip the display (bypassing any requirement for an X11 server or GUI toolkits). It silently processes the video mathematically and saves the final product to a new file, which is highly required for remote server evaluation tasks.
```bash
python main.py --input test_video.mp4 --output final_result.mp4
```
