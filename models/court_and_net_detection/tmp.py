import cv2
import numpy as np
import matplotlib.pyplot as plt

# Your existing court_info and net_info data
court_info = [
    [900, 883],
    [2008, 883],
    [799, 1198],
    [2125, 1198],
    [625, 1722],
    [2314, 1722]
]

court_info = np.array(court_info, np.int32)

# Sort points by y-coordinate first, then x-coordinate
court_info = sorted(court_info, key=lambda p: (p[1], p[0]))
# Load the video file
video_path = '../../utils/footages/short.mp4'  # Replace with your video path
cap = cv2.VideoCapture(video_path)

# Read the first frame from the video
ret, frame = cap.read()

if not ret:
    print("Failed to read the video frame.")
    cap.release()
    exit()

# Convert coordinates to numpy arrays for drawing lines
shift_amount = 20  # Amount to shift, adjust this value as needed

# Shift top corners (assuming first two points are the top corners)
court_info[0][1] -= shift_amount  # Shift first upper corner upwards
court_info[1][1] -= shift_amount  # Shift second upper corner upwards

# Shift bottom corners (assuming last two points are the bottom corners)
court_info[-2][1] += shift_amount  # Shift first lower corner downwards
court_info[-1][1] += shift_amount  # Shift second lower corner downwards

# Convert coordinates to numpy arrays for drawing lines
court_info = np.array(court_info, np.int32)

# Extract the bounding box of the court (the rectangle)
x_min = min(court_info[:, 0])
x_max = max(court_info[:, 0])
y_min = min(court_info[:, 1])
y_max = max(court_info[:, 1])

# Crop the region of interest (ROI) from the frame
roi = frame[y_min:y_max, x_min:x_max]

# Convert the ROI to grayscale
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150, apertureSize=3)

# Apply Hough Line Transform to detect lines
lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)

# Merge lines with similar y-coordinates within a threshold
y_threshold = 10  # Set the threshold for merging lines
final_court_lines=[]
if lines is not None:
    # Dictionary to store merged lines by y-coordinate range
    merged_lines = {}

    for line in lines:
        x1, y1, x2, y2 = line[0]
        
        # Check if the line is horizontal (or nearly horizontal)
        if abs(y1 - y2) < 10:  # Tolerance for slight slope
            
            # Calculate the length of the line
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            
            # Draw the line only if the length is greater than 50 pixels
            if length > 150:
                # Find a close y-coordinate group to merge with
                merged = False
                for y_key in merged_lines:
                    if abs(y1 - y_key) <= y_threshold:
                        merged_lines[y_key].append((x1, x2))
                        merged = True
                        break

                if not merged:
                    merged_lines[y1] = [(x1, x2)]

    # Draw the merged lines
    for y, x_ranges in merged_lines.items():
        min_x = min(min(x_range) for x_range in x_ranges)
        max_x = max(max(x_range) for x_range in x_ranges)
        
        # Adjust coordinates back to the original frame
        min_x += x_min
        max_x += x_min
        y += y_min
        
        # Draw the merged line on the original frame
        cv2.line(frame, (min_x, y), (max_x, y), (0, 255, 0), 2)
        final_court_lines.append([(min_x,y),(max_x,y)])

# Display the frame with the detected lines
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.title("Merged Horizontal Lines Inside Adjusted Court")
plt.axis('off')
plt.show()

# Release the video capture object
cap.release()