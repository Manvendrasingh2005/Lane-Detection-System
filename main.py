import cv2
import numpy as np
import sys

def canny_edge_detector(image):
    """
    Applies Gaussian Blur and Canny edge detection.
    """
    # Convert image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    # Apply Canny edge detection
    canny = cv2.Canny(blur, 50, 150)
    return canny

def region_of_interest(image):
    """
    Restricts the edge detected image to a dynamic triangular region
    that typically corresponds to the lane area in front of the car.
    """
    height = image.shape[0]
    width = image.shape[1]
    
    # Define a polygon (triangle/trapezoid) for the region of interest
    polygons = np.array([
        [(int(width * 0.1), height), 
         (int(width * 0.9), height), 
         (int(width * 0.5), int(height * 0.55))]
    ])
    
    # Create a blank mask
    mask = np.zeros_like(image)
    
    # Fill the polygon on the mask
    cv2.fillPoly(mask, polygons, 255)
    
    # Bitwise AND between the image and mask to isolate region
    masked_image = cv2.bitwise_and(image, mask)
    return masked_image

def create_coordinates(image, line_parameters):
    """
    Given a slope and intercept, calculates the endpoints of a line 
    touching the bottom and extending to ~3/5 of the image height.
    """
    try:
        slope, intercept = line_parameters
    except TypeError:
        slope, intercept = 0.001, 0  # Fallback to avoid crashes
        
    y1 = image.shape[0]
    y2 = int(y1 * (3.5/5))  # Make lines end higher up on the screen
    
    # Calculate x coordinates
    x1 = int((y1 - intercept) / slope) if slope else 0
    x2 = int((y2 - intercept) / slope) if slope else 0
    
    return np.array([x1, y1, x2, y2])

def average_slope_intercept(image, lines):
    """
    Classifies lines into left and right lanes based on slope, 
    and averages them into a single line per side.
    """
    left_fit = []
    right_fit = []
    
    if lines is None:
        return None
        
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        
        # Fit a linear polynomial and return slope and intercept
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        intercept = parameters[1]
        
        # Determine left or right based on slope
        if slope < -0.3: # Negative slope corresponds to left lane (due to positive y pointing downwards)
            left_fit.append((slope, intercept))
        elif slope > 0.3: # Positive slope corresponds to right lane
            right_fit.append((slope, intercept))
            
    # Calculate average slopes and intercepts
    left_fit_average = np.average(left_fit, axis=0) if len(left_fit) > 0 else None
    right_fit_average = np.average(right_fit, axis=0) if len(right_fit) > 0 else None
    
    line_arr = []
    if left_fit_average is not None:
        left_line = create_coordinates(image, left_fit_average)
        line_arr.append(left_line)
    if right_fit_average is not None:
        right_line = create_coordinates(image, right_fit_average)
        line_arr.append(right_line)
        
    return np.array(line_arr)

def display_lines(image, lines):
    """
    Draws the averaged lines on a blank image.
    """
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line
            # Draw line on the blank image
            cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 10)
    return line_image

def process_frame(frame):
    """
    Runs the complete lane finding pipeline on a single frame.
    """
    # Resize frame for consistency, useful for generalized ROI
    # We will keep original size but it's good practice for varying inputs
    # frame = cv2.resize(frame, (1280, 720))
    
    # 1. Edge Detection
    canny_image = canny_edge_detector(frame)
    
    # 2. Region of Interest
    cropped_image = region_of_interest(canny_image)
    
    # 3. Hough Transform
    # rho=2, theta=1 degree, threshold=100 (min intersections), minLineLength=40, maxLineGap=5
    lines = cv2.HoughLinesP(
        cropped_image, 
        rho=2, 
        theta=np.pi/180, 
        threshold=50, 
        lines=np.array([]), 
        minLineLength=40, 
        maxLineGap=150
    )
    
    # 4. Filter and average lines
    averaged_lines = average_slope_intercept(frame, lines)
    
    # 5. Draw lines
    line_image = display_lines(frame, averaged_lines)
    
    # 6. Overlay on original frame
    combo_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    
    return combo_image

def main():
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        video_path = "test_video.mp4"
        
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video '{video_path}'")
        print("Please check if the file exists or pass it as an argument: python main.py <video_path>")
        sys.exit(1)
        
    print(f"Successfully opened '{video_path}', processing...")
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            # End of video stream
            break
            
        processed_frame = process_frame(frame)
        
        # Display the result
        cv2.imshow("Lane Detection Result", processed_frame)
        
        # Press 'q' to exit early
        # Note: cv2.waitKey(25) waits 25ms between frames (~40fps)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
            
    print("Finished processing video.")
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
