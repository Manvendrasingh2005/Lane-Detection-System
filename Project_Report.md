# Lane Detection System: Project Report

**Author**: Manvendrasingh2005 

## 1. Abstract
The goal of this project is to construct a scalable software module capable of real-time lane detection using traditional computer vision principles. The system addresses a primary necessity of autonomous driving architectures: accurately interpreting infrastructural boundaries. By establishing a robust pipeline—composed of grayscaling, Gaussian smoothing, edge detection, regional masking, and Hough transforms—the application successfully traces solid mathematical lines over a dynamic video feed without reliance on deep neural networks.

## 2. Introduction
Lane detection systems represent one of the absolute fundamental requirements in modern Advanced Driver Assistance Systems (ADAS). A vehicle's onboard processing unit must continually interpret the spatial environment around it. This project relies strictly on image processing methodology (utilizing the open-source library OpenCV) over neural network computation to demonstrate a clear programmatic understanding of core algorithms. As specified in the syllabus, the objective encompasses the development of a fully executable algorithm directly capable of operating in a completely headless environment (CLI native).

## 3. Methodology

### A. Pre-Processing (Grayscale and Gaussian Blur)
Camera feeds arrive in three-channel format (Red, Green, Blue) capturing unnecessary complexities like shadow gradients, chromatic aberrations, and distracting environment features. The first mathematical step involves standardizing the input matrix to a single channel (Grayscale). Subsequently, high-frequency noise is suppressed using a $5 \times 5$ Gaussian kernel convolution, effectively blending disparate pixel artifacts into an organic, smooth image suitable for derivative calculation.

### B. Canny Edge Detection
The Canny algorithm parses the smoothed image to calculate pixel intensity gradients natively. High differential changes (e.g., jumping from dark asphalt pixel values to bright white line values) trigger the algorithm to categorize specific pixels as "edges". We calibrated the hysteresis thresholds to $50_{min}$ and $150_{max}$, which yielded optimum tracking sensitivity on the standard dashcam datasets while discarding weak artifacts (e.g., cracks in the concrete).

### C. Region of Interest Selection (Masking)
The primary hazard during lane detection is computational distraction. Edges are detected everywhere—on oncoming vehicles, clouds in the sky, and objects in adjoining tracks. To counteract this, the software applies a dynamic geometrical mask corresponding to the perspective projection of the lane immediately occupying the vehicle’s trajectory. A triangle/trapezoidal bitwise mask zeroes out all matrix elements unassociated with the lower section of the roadway matrix.

### D. Probabilistic Hough Line Transform
Working with binary edge data obtained from the Canny stage, the script must geometrically combine the disconnected pixel points. By executing `cv2.HoughLinesP`, the edges are mathematically transitioned from the spatial Cartesian plane ($y = mx + b$) onto the Hough parameters ($\rho, \theta$). Intersections in Hough Space indicate mathematical collinearity. Thus, the system groups corresponding pixels into continuous line segments.

## 4. Implementation details
The core execution occurs within `main.py`, encapsulated to support highly-flexible `argparse` triggers. 
1. `canny_edge_detector(image)` encapsulates stages A & B.
2. `region_of_interest(image)` applies the geometric polygon slice.
3. `average_slope_intercept()` represents the highest functional intelligence in this module, mapping positive slopes (the mathematical right lane) and negative slopes (left lane) to compute the continuous average parameters required avoiding jagged artifact mapping on video feeds.
4. `--output` argument integrates OpenCV’s `VideoWriter`, bypassing `cv2.imshow` requests ensuring execution compatibility in UI-less Unix testing servers.

## 5. Reflection and Conclusion
The implementation was notably robust against standard road configurations. 

**Limitations:** The current architecture heavily presumes linear vectors; highly banked or curved roads occasionally out-scale the single-degree polynomial constraint applied. Furthermore, extreme chromatic saturation shifts (from tunnels to heavy sunlight glare) can occasionally mask lane contours to the Canny detector limit because grayscaling erases all color frequency differentiation.

**Syllabus Fulfillment:** This logic firmly illustrates competency in sequential array manipulation (`NumPy`), implementation constraints, structural error handling (`argparse` & Exception handling bounds), and mathematical modeling. The resultant product cleanly fulfills execution limits safely and rapidly.
