# SpeedAndDistance_Estimator

`SpeedAndDistance_Estimator` is a class defined in the file [speed_n_distance.py](speed_n_distance.py). It provides functionalities to estimate and visualize the speed and distance traveled by players in a video sequence. This is particularly useful for analyzing player movement and performance in sports applications. Below is a detailed description of the class and its functions, highlighting any unique features and key functionalities.

### Key Functionalities:

1. **Speed and Distance Estimation for Doubles:**
   - **Function:** `speed_n_distance_doubles(self, detected_players)`
   - **Description:** Estimates the speed and distance traveled by each player during a doubles game. It calculates these metrics over a defined window of frames, considering the position of players within the court boundaries.
   - **Unique Feature:**
     - **Court Boundaries Checking:** The function ensures that the player’s coordinates are within the court’s boundary before calculating the distance and speed. This prevents erroneous data due to out-of-bounds positions and enhances the accuracy of speed and distance measurements.

2. **Speed and Distance Estimation:**
   - **Function:** `speed_n_distance(self, detected_players)`
   - **Description:** Calculates the speed and distance for each player based on their positions in each frame. This method operates over a frame window and updates player statistics accordingly.
   - **Key Functionality:**
     - **Pixel-Based Speed Calculation:** Speed is computed in pixels per frame, which is useful when working with video frames where exact distance metrics in real-world units (like meters) are not directly available.

3. **Drawing Speed and Distance on Frames:**
   - **Function:** `draw_speed_and_distance(self, frames, detected_players)`
   - **Description:** Annotates each video frame with the speed (in km/hr) and distance (in meters) traveled by each player. This helps in visualizing player performance directly on the video.
   - **Key Functionality:**
     - **Foot Positioning:** The function uses `get_foot_position()` to determine the best location on the frame to display the player’s speed and distance. This ensures that the annotations are placed in a readable position relative to the player’s bounding box.

### Supporting Functions:

1. **`measure_distance(start_position, end_position)`**
   - **Function:** Calculates the distance between two positions in the video frame.
   - **Description:** This utility function is crucial for computing how far a player has moved between frames. It provides the distance covered by the player in pixels, which is then used to calculate speed.

2. **`get_foot_position(bbox)`**
   - **Function:** Determines the position on the frame where the player's foot is likely located.
   - **Description:** Helps in positioning the speed and distance text on the frame so that it is close to the player’s actual location. This ensures that the annotations are visually aligned with the player’s position.

### Unique Features and Enhancements:

- **Court Boundaries Check:**
  - The `speed_n_distance_doubles` method incorporates a check to ensure that players' movements are within the court's boundaries. This adds an extra layer of validation to ensure that the measurements are meaningful and accurate.

- **Frame Window-Based Calculation:**
  - Both `speed_n_distance_doubles` and `speed_n_distance` methods utilize a sliding window approach to compute speed and distance. This approach helps smooth out fluctuations in speed calculations and provides more stable metrics over a series of frames.

- **Visual Annotations:**
  - The `draw_speed_and_distance` method not only calculates but also visualizes the speed and distance data on the video frames. This is particularly useful for real-time analysis and post-game reviews.
