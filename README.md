# Real-Time Lane Detection System

A Python-based lane detection implementation using computer vision techniques like Canny Edge Detection and Hough Transform.

## Features
- Grayscale Conversion
- Gaussian Blur
- Canny Edge Detection
- Dynamically calculated Region of Interest (ROI)
- Hough Transform for Line Detection
- Slope/Intercept filtering and averaging

## Prerequisites

1. Python 3.7+
2. OpenCV and NumPy (`opencv-python`, `numpy`)

## Quickstart

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the detection on a sample video:
   ```bash
   python main.py test_video.mp4
   ```
   *(Note: Provide the path to your valid video file)*
