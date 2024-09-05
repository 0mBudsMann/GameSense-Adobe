import cv2
import numpy as np
import matplotlib.pyplot as plt

# JSON data with coordinates
court_info = [
    [729, 544],
    [1134, 544],
    [1185, 688],
    [649, 688],
    [479, 990],
    [1267, 990]
]

net_info = [
    [598, 528],
    [598, 688],
    [1234, 688],
    [1234, 528]
]

# Load the video file
video_path = './videos/test5.mp4'  # Replace with your video path
cap = cv2.VideoCapture(video_path)

# Read the first frame from the video
ret, frame = cap.read()

if not ret:
    print("Failed to read the video frame.")
    cap.release()
    exit()

# Convert coordinates to numpy arrays for drawing lines
court_info = np.array(court_info, np.int32)
net_info = np.array(net_info, np.int32)

# Draw lines between all points in court_info
for i in range(len(court_info)):
    for j in range(i + 1, len(court_info)):  # Start from i + 1 to avoid drawing line twice for the same pair
        cv2.line(frame, tuple(court_info[i]), tuple(court_info[j]), (0, 255, 0), 2)  # Green for court

# Draw lines between all points in net_info
for i in range(len(net_info)):
    for j in range(i + 1, len(net_info)):  # Start from i + 1 to avoid drawing line twice for the same pair
        cv2.line(frame, tuple(net_info[i]), tuple(net_info[j]), (0, 0, 255), 2)  # Red for net

# Display the frame with the drawn court and net
plt.figure(figsize=(10, 6))
plt.imshow(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
plt.title("Court and Net Overlay on Video Frame")
plt.axis('off')
plt.show()

# Release the video capture object
cap.release()

