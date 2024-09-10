# PlayerTracker

`PlayerTracker` is a class inside the file [player_tracking.py](player_tracking.py). It is designed for detecting, tracking, and annotating players in video frames using the YOLO model. The class provides functionalities for detecting players in real-time, drawing bounding boxes around them, and saving the results for later use. Below is a breakdown of its key functions and their descriptions:

### Key Functions

1. **`__init__(self, model_path)`**:
   - Initializes the `PlayerTracker` class.
   - Loads the YOLO model from the provided `model_path`.
   - **Unique Feature**: By using the `ultralytics` YOLO model, this class supports highly optimized real-time player detection and tracking.

2. **`detect_frames(self, frames, read_from_record=False, record_path=None)`**:
   - Detects players in multiple video frames.
   - **Key Functionality**:
     - **Real-time Detection**: It processes each frame to detect the presence of players, allowing the system to handle live video streams.
     - **Optimized for Speed**: If `read_from_record` is set to `True` and a `record_path` is provided, the method reads the preprocessed player data from a `pkl` file, skipping detection to save processing time.
     - Saves detected player data to a `.pkl` file for future use, reducing preprocessing time in subsequent runs.
   
3. **`detect_frame(self, frame)`**:
   - Detects players in a single frame.
   - **Key Functionality**:
     - Uses the YOLO model to track and detect objects in each frame.
     - Stores the `track_id`, `coordinates`, and `class_id` (object class) for each detected player in a dictionary.
     - **Unique Feature**: YOLO’s real-time tracking ensures that player movements are accurately captured frame by frame, making it highly suitable for live match analysis.

4. **`draw_boxes(self, frames, detected_players)`**:
   - Draws bounding boxes around detected players in each frame.
   - **Key Functionality**:
     - Loops through frames and overlays bounding boxes around players using the player detection data.
     - Annotates each player with their respective `track_id`.
     - **Unique Feature**: The bounding boxes and annotations are drawn in real time to provide immediate visual feedback during the video analysis.
     - Uses OpenCV functions to customize the appearance of boxes and text, maintaining a clear and readable display.

5. **`save_player_data(self, detected_players, file_path)`**:
   - Saves player detection data to a JSON file.
   - **Key Functionality**:
     - Writes player coordinates and metadata into a structured JSON format for each frame.
     - **Unique Feature**: This ensures that player data can be used later for analytics or reprocessing without needing to rerun detection.

### Real-Time Behavior

Real-time performance is maintained throughout the code in several ways:
- **YOLO Model**: The `ultralytics` YOLO model used for detection is designed for fast inference, ensuring that the detection process occurs without delays, even in live streams.
- **Data Caching**: The ability to save and load player data from `pkl` files allows the system to bypass redundant computations, speeding up subsequent processes.
- **Frame-by-Frame Processing**: Each function processes frames independently, ensuring smooth operation during live feeds or batch processing of recorded video.
- **Real-Time Annotations**: The bounding boxes and player IDs are drawn in real-time on the frames, ensuring that the system provides immediate feedback without any post-processing delay.

# Doubles_Tracking

`Doubles_Tracking` is a class inside the file [doubles_tracking.py](doubles_tracking.py). It is designed to track players during a badminton doubles match, using the YOLO model to detect players and the net/court boundaries. This class handles player detection, tracking, annotation, and data storage for real-time analysis. Below is a breakdown of its key functions and features:

### Key Functions

1. **`__init__(self, model_path)`**:
   - Initializes the `Doubles_Tracking` class.
   - Loads the YOLO model from the specified `model_path` for detecting players.
   - **Unique Feature**: By using the `ultralytics` YOLO model, the class supports efficient real-time player detection and tracking in doubles matches.

2. **`detect_frames(self, frames, read_from_record=False, record_path=None)`**:
   - Detects players in multiple frames.
   - **Key Functionality**:
     - **Real-time Detection**: Processes each frame to detect players, allowing the system to handle live video streams.
     - **Optimized for Speed**: If `read_from_record` is set to `True` and a `record_path` is provided, the method reads the preprocessed player data from a `pkl` file, reducing the need for reprocessing.
     - Saves detected player data to a `.pkl` file to speed up future runs and avoid redundant computations.

3. **`detect_frame(self, frame)`**:
   - Detects players in a single frame.
   - **Key Functionality**:
     - Uses the YOLO model to detect and track players.
     - Stores `track_id`, `coordinates`, and `class_id` for detected players.
     - **Unique Feature**: Only "person" class objects are tracked, ensuring that only players are detected and other irrelevant objects are ignored.

4. **`draw_boxes(self, frames, detected_players)`**:
   - Draws bounding boxes around detected players in each frame and annotates their team based on the court location.
   - **Key Functionality**:
     - Adds visual annotations to the video frames, marking the court and net boundaries for context.
     - Distinguishes between two teams (Team 1 and Team 2) based on the position relative to the net.
     - **Unique Feature**:
       - Coordinates for the court and net are predefined and overlaid on the frames using red circles to visualize the game boundaries.
       - Players from **Team 1** (above the net) are marked with red boxes, and players from **Team 2** (below the net) are marked with blue boxes.
     - Real-time feedback through visual annotations allows for immediate analysis of players' positions.

5. **`save_player_data(self, detected_players, file_path)`**:
   - Saves the detected player data to a JSON file for further analysis or reuse.
   - **Key Functionality**:
     - Organizes player data frame by frame, with `track_id`, coordinates, and other relevant metadata.
     - Saves this data in a structured format (JSON), which can be used later without reprocessing the video.

### Real-Time Behavior

The code is optimized to maintain real-time behavior through several mechanisms:
- **YOLO Model**: The `ultralytics` YOLO model used for player detection and tracking is known for its fast inference speed, ensuring that players are detected and tracked with minimal delay.
- **Data Caching**: The ability to read from preprocessed data files (`pkl`) minimizes redundant computations and speeds up detection, allowing for faster processing in future runs.
- **Frame-by-Frame Processing**: Each function processes frames independently, ensuring that the system can handle live video streams or batch process pre-recorded matches with real-time feedback.
- **Real-Time Annotations**: Visual boxes and annotations, including team distinctions and court boundaries, are drawn in real-time on the frames, ensuring immediate feedback and analysis during a match.

# real_time_detection_and_tracking

`real_time_detection_and_tracking` is a key function located in the file [kalman_filter_tracking_2](kalman_filter_tracking_2.py). It provides an efficient, real-time system for tracking the shuttlecock during a badminton match, while also tracking its speed, determining rest states, detecting rallies, and calculating the score. Below is an in-depth look at the key functionalities, supporting functions, and unique aspects of this tracking system.

### Key Functionalities:

1. **Real-time Detection and Tracking:**
   - The function processes frames in real-time to detect and track the shuttlecock. Each frame is passed through a pre-trained object detection model that detects the shuttle and extracts its coordinates.
   - **Unique Feature:** 
     - The system filters out stationary objects (e.g., net posts) using a customizable blacklist, ensuring accurate shuttle detection and avoiding false positives. This is dynamically done by comparing detected positions with known stationary objects in the blacklist.

2. **Kalman Filter for Smooth Tracking:**
   - The **Kalman Filter** is utilized to predict the next position of the shuttlecock based on its previous positions, making the system resilient to noisy detections or occasional misdetections by the model.
   - **Key Functionality:**
     - The filter smooths the shuttle's trajectory, predicting where it will likely be in the next frame. This allows for continuous tracking, even when the model momentarily loses track of the shuttle, making the system robust in real-time applications.

3. **Blacklist Mechanism (Avoiding Stationary Objects):**
   - A key feature is the dynamic creation and use of a `black_list` to avoid detecting static objects like the net or other obstacles. This reduces false positives in shuttle detection.
   - **Unique Feature:** 
     - The function automatically detects and filters out stationary objects during the game, ensuring that only the shuttle's movement is tracked. The function `is_close_to_blacklist()` ensures that objects close to blacklist coordinates are excluded from tracking.

4. **Speed Calculation:**
   - For each detected shuttle position, the function calculates its speed by analyzing how far the shuttle moves between frames and factoring in the frame rate (`fps`).
   - **Key Functionality:**
     - The speed is derived from the difference in shuttle position between two consecutive frames, ensuring real-time tracking of shuttle speed, providing valuable information about the shuttle’s velocity during play.

5. **Relay Detection:**
   - The function detects when a rally (relay) starts and ends based on shuttle movement patterns. If the shuttle is consistently moving upwards or downwards, the relay is considered active. When the shuttle stops moving (rest state), the relay is marked as finished.
   - **Unique Feature:** 
     - The system detects when a relay starts and ends without any external triggers. It uses shuttle position history and velocity to determine the start and stop points dynamically in real-time.
   - **Key Functionality:**
     - The function tracks the state of play by analyzing consistent changes in shuttle height and speed, helping identify when a player hits the shuttle and when it lands.

6. **Rest State Detection:**
   - If the shuttle stays in a fixed position for a certain number of frames, the system detects that the shuttle is at rest.
   - **Unique Feature:** 
     - A **Rest Threshold** is set for detecting when the shuttle is at rest (e.g., after 3 consecutive frames). This allows the system to autonomously understand when a point in the game is over without manual intervention.

7. **Real-time Scoring System:**
   - As soon as the shuttle comes to rest, the system evaluates its final position to calculate whether the shuttle landed in or outside the court, and scores are updated for the respective player.
   - **Key Functionality:**
     - The scoring logic dynamically assesses the final landing position of the shuttle by checking its location relative to predefined court boundaries. Points are assigned to the player on the opposite side of the landing position.

8. **Real-time Visualization:**
   - The function overlays crucial information directly on the video frames, such as:
     - The speed of the shuttle.
     - Whether the shuttle is at rest.
     - Relay status (active/inactive).
     - Player scores.
   - **Key Functionality:**
     - The shuttle's current speed and coordinates are displayed frame by frame in real time, giving immediate visual feedback to the user. This makes it easier to track gameplay in both real-time and post-game analysis.

9. **Stationary Object Detection:**
   - The system identifies stationary objects in the frame and marks their locations. This is done using a function that analyzes the frequency of specific coordinates over time.
   - **Unique Feature:** 
     - It dynamically identifies and records stationary objects during the game, automatically creating a blacklist to ignore these objects in future frames.

### Supporting Functions and Their Key Role:

1. **`is_close_to_blacklist(coord, black_list, threshold=15)`:**
   - This function ensures that detected coordinates are not mistakenly classified as the shuttle if they are near known stationary objects, helping to reduce false positives.

2. **`determine_shooter(prev_k_frame.copy())`:**
   - Determines which player hit the shuttle based on its trajectory (upward or downward movement). This function helps in real-time detection of which player is responsible for hitting the shuttle.

3. **`is_shuttle_in_rest(shuttle_coords_queue, 5)`:**
   - Checks whether the shuttle is in a rest state (i.e., not moving) by analyzing the recent position history. It ensures the system correctly identifies when a rally ends.

4. **`assign_points(shuttle_position, prev_k_frame.copy())`:**
   - Determines the landing position of the shuttle to assign points to the correct player. This function checks if the shuttle landed inside or outside the court, facilitating the scoring system.

5. **`group_similar_coordinates(current_coords, threshold=10)`:**
   - Groups nearby detected shuttle positions to avoid multiple redundant detections. This function helps maintain tracking accuracy by consolidating detections into a single shuttle position.

6. **`identify_stationary_objects()`:**
   - Identifies stationary objects on the court by analyzing frequently detected coordinates that don't move. These objects are then added to the blacklist.

7. **`draw_shuttle_predictions(frames, tracking_data)`:**
   - Draws shuttle positions on the frames based on the tracking data, showing real-time shuttle trajectory, speed, and rest state on the video output.

8. **`interpolate_shuttle_tracking(tracking_data)`:**
   - Smoothens tracking data by interpolating any missing positions to ensure continuous shuttle tracking. This is critical for cases where the model may miss detecting the shuttle in a few frames.

### Unique Features and Enhancements:

- **Kalman Filter for Real-time Smooth Tracking:**
   - The integration of the Kalman Filter enhances the robustness of the tracking system. It allows for smooth and continuous tracking, even in cases where the model fails to detect the shuttle momentarily.
  
- **Dynamic and Autonomous Scoring System:**
   - The real-time detection of rally start and end, combined with an automatic scoring mechanism, ensures that the game progresses without requiring manual input or external triggers.

- **Stationary Object Filtering:**
   - The system intelligently identifies and filters stationary objects, significantly improving tracking accuracy by preventing false positives near known obstacles.

- **Real-time Relay Detection and Visualization:**
   - The system dynamically tracks each relay’s duration and visualizes the entire gameplay, including shuttle speed, position, and scores, in real time. This provides instant feedback on the gameplay.

- **Realistic Speed Calculation:**
   - Shuttle speed is calculated based on real-world court dimensions and frame rate, providing a realistic measure of the shuttle’s velocity during play.

### Real-time Behavior:
- The system processes each frame as it is received, immediately updating shuttle positions, speeds, rest states, and scores, ensuring that all game-related metrics are tracked and updated in real time.
- Visualization overlays on the video show the shuttle’s trajectory, relay status, and score updates as they happen, providing instant feedback on the gameplay.
