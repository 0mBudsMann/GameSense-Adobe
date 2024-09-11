import cv2
import numpy as np
import matplotlib.pyplot as plt

# Your existing court_info and net_info data
court_info = [[823, 889], [823, 1216], [2141, 1216], [2141, 889]]

court_info = np.array(court_info, np.int32)

# Sort points by y-coordinate first, then x-coordinate
court_info = sorted(court_info, key=lambda p: (p[1], p[0]))
# Load the video file
video_path = '../../utils/footages/short_shuttle.mp4'  # Replace with your video path
cap = cv2.VideoCapture(video_path)

# Read the first frame from the video
ret, frame = cap.read()

if not ret:
    print("Failed to read the video frame.")
    cap.release()
    exit()
for point in court_info:
        cv2.circle(frame, tuple(point), radius=55, color=(0, 255, 0), thickness=-1)  # Green filled circles
# Convert coordinates to numpy arrays for drawing lines
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.title("Merged Horizontal Lines Inside Adjusted Court")
plt.axis('off')
plt.show()

# Release the video capture object
cap.release()