import cv2
import numpy as np
import json

def draw_court_and_net_on_frames(frames):
    with open('./res/courts/courts_kp/coordinates.json', 'r') as file:
        data = json.load(file)

    court_info = data['court_info']
    net_info = data['net_info']

    # Convert coordinates to numpy arrays for drawing lines
    court_info = np.array(court_info, np.int32)
    net_info = np.array(net_info, np.int32)

    # Process each frame
    processed_frames = []
    for frame in frames:
        # Draw lines between all points in court_info
        for i in range(len(court_info)):
            for j in range(i + 1, len(court_info)):  # Start from i + 1 to avoid drawing line twice for the same pair
                cv2.line(frame, tuple(court_info[i]), tuple(court_info[j]), (0, 255, 0), 2)  # Green for court

        # Draw lines between all points in net_info
        for i in range(len(net_info)):
            for j in range(i + 1, len(net_info)):  # Start from i + 1 to avoid drawing line twice for the same pair
                cv2.line(frame, tuple(net_info[i]), tuple(net_info[j]), (0, 0, 255), 2)  # Red for net

        # Append the processed frame to the list
        processed_frames.append(frame)

    return processed_frames