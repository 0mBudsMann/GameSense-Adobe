from collections import deque, Counter
import cv2

import pandas as pd
import numpy as np
import cv2
import torch
import torch
from ultralytics import YOLO

model = YOLO(r'models\shuttle_detection\weights\best.pt')  # Ensure you have the correct model file
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)


def group_similar_coordinates(coords, threshold=10):
    """
    Groups coordinates that are within a threshold distance from each other.
    Returns a list of unique coordinates (averaged within the group).
    Also updates the global frequency dictionary.
    """
    grouped_coords = []
    used = [False] * len(coords)

    for i in range(len(coords)):
        if used[i]:
            continue

        # Start a new group with the current coordinate
        current_group = [coords[i]]
        used[i] = True

        for j in range(i + 1, len(coords)):
            # Compute the Euclidean distance between coordinates
            dist = np.linalg.norm(np.array(coords[i]) - np.array(coords[j]))
            if dist < threshold:
                current_group.append(coords[j])
                used[j] = True

        # Average the grouped coordinates
        avg_coord = tuple(np.mean(current_group, axis=0))
        grouped_coords.append((avg_coord, len(current_group)))

        # Update global coordinate frequency
        if avg_coord in global_coord_frequency:
            global_coord_frequency[avg_coord] += len(current_group)
        else:
            global_coord_frequency[avg_coord] = len(current_group)

    return grouped_coords

def identify_stationary_objects(threshold=10):
    """
    Identifies stationary objects by grouping similar coordinates based on frequency of occurrence
    and merging those that are close together.
    """
    global global_coord_frequency, stationary_coords

    # Get the list of coordinates and their frequencies from the global frequency dictionary
    coords_with_freq = list(global_coord_frequency.items())

    def group_coordinates_by_proximity(coords_with_freq, threshold):
        """
        Groups coordinates in the global frequency dictionary by proximity and sums their frequencies.
        """
        grouped_freq = []
        used = [False] * len(coords_with_freq)

        for i in range(len(coords_with_freq)):
            if used[i]:
                continue

            current_group = [coords_with_freq[i][0]]  # Start a new group with the current coordinate
            total_freq = coords_with_freq[i][1]  # Initialize total frequency with current frequency
            used[i] = True

            for j in range(i + 1, len(coords_with_freq)):
                # Compute the Euclidean distance between the coordinates
                dist = np.linalg.norm(np.array(coords_with_freq[i][0]) - np.array(coords_with_freq[j][0]))
                if dist < threshold:
                    current_group.append(coords_with_freq[j][0])
                    total_freq += coords_with_freq[j][1]
                    used[j] = True

            # Average the grouped coordinates
            avg_coord = tuple(np.mean(current_group, axis=0))
            grouped_freq.append((avg_coord, total_freq))

        return grouped_freq

    # Group the coordinates by proximity
    grouped_coords_with_freq = group_coordinates_by_proximity(coords_with_freq, threshold)

    # Define a threshold for considering an object stationary based on frequency
    stationary_threshold = 5  # You can adjust this value
    print(grouped_coords_with_freq)
    # Find coordinates that occur above the threshold and add to stationary_coords
    stationary_coords = [(coord,freq) for coord, freq in grouped_coords_with_freq if freq > stationary_threshold]
    
    return stationary_coords

# Global variables to track coordinate frequencies and stationary object coordinates
global_coord_frequency = {}
stationary_coords = []  # List to store coordinates of detected stationary objects
score = [0,0]
prev_k_frame = deque(maxlen=10)

def real_time_detection_and_tracking(video_path):
    global global_coord_frequency, stationary_coords

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"FPS: {fps}")

    ret, frame = cap.read()
    frame_height, frame_width = frame.shape[:2]
    out = cv2.VideoWriter('realtime_tracking_kalman.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    # Dictionary to store tracking data
    tracking_data = {}
    coord_counter = Counter()  # Directly maintain a counter for coordinates
    frame_count = 0
    shuttle_coords_queue = deque(maxlen=5) 
    prev_k_frame = deque(maxlen=10)
    scored = False
    
    black_list = [(638.8124256963315, 350.4730038850204), (291.1255159378052, 142.9724564552307)]
    rest_coords = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Run object detection on the current frame (replace with your model inference)
        results = model([frame])
        print(frame_count)
        
        # Assuming YOLO model results
        boxes = results[0].boxes.xyxy.cpu().numpy()  # Get the bounding boxes
        class_ids = results[0].boxes.cls.cpu().int().numpy()  # Get the class IDs
        scores = results[0].boxes.conf.cpu().numpy()  # Get the confidence scores

        # Convert detection results into a DataFrame
        df_current = pd.DataFrame({
            'xmin': boxes[:, 0],
            'ymin': boxes[:, 1],
            'xmax': boxes[:, 2],
            'ymax': boxes[:, 3],
            'class_id': class_ids,
            'confidence': scores
        })

        # Initialize a list to collect the current frame's coordinates for grouping
        current_coords = []

        for _, row in df_current.iterrows():
            coord = [(row['xmin'] + row['xmax']) / 2, (row['ymin'] + row['ymax']) / 2]  # Object center coordinates

            # Only track specific class (e.g., class_id == 0 for a ball/shuttlecock)
            if row['class_id'] == 0:
                current_coords.append(coord)
                shuttle_coords_queue.append(coord)
                prev_k_frame.append(coord)
                
                
        tmp_img = frame.copy()
                
        group = group_similar_coordinates(current_coords)          
    
        dummy = 10
        for x,y in current_coords:
            cv2.rectangle(tmp_img, (int(x)-dummy, int(y)-dummy),
                      (int(x)+dummy, int(y)+dummy), (255, 0, 100), 2)
        
            
        cv2.imwrite("tmp_img.jpg",tmp_img)
        out.write(tmp_img)
        # if len(rest_coords)>1: break
        frame_count += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()


    # Identify stationary objects based on frequency
    stationary_coords = identify_stationary_objects()
    print("Stationary coordinates detected:")
    print(stationary_coords)
    
    return stationary_coords

# Example usage
# real_time_detection_and_tracking("video.mp4", "tracking_data.json")
real_time_detection_and_tracking(r"C:\Users\Lenovo\Desktop\test\no_drop_small.mp4")