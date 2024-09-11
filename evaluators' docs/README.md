# 1) GAME SELECTION AND PLAYER AREA MARKING


## Game Chosen: Badminton

- **Why We Chose Badminton Over TT and Tennis**  
  We chose badminton because it offers the right mix of challenges for real-time detection. The game has a medium-sized court and fast gameplay, making it perfect for testing our detection models. TT has quick movements in a small area, while tennis covers a large area but moves more slowly. Badminton strikes a balance, with complex player movements and shuttlecock trajectories, making it an ideal choice. It’s also a popular sport with a growing need for automated analysis tools in training and match reviews.

## Net and Court Detection

- **Model Selection: RCNN vs. YOLO**  
  For detecting the net and court, we considered two popular models: YOLO and RCNN. YOLO is known for its speed, which is great for real-time tasks, but **accuracy was our top priority** since all further analysis relies on getting this part right. Because we only needed to detect the net and court in one frame, time wasn’t a big concern, so we chose RCNN. RCNN is known for its **robustness**, meaning it’s excellent at accurately detecting objects, even under different conditions like lighting and angles.


## Player Detection

- **YOLO Implementation**  
  For detecting players, we used YOLO because it’s fast, which is crucial for real-time analysis. We trained YOLO on a powerful NVIDIA 4090 GPU (courtesy to one of our professors for lending us the GPU), allowing us to handle large datasets quickly. YOLO’s speed ensures we can keep up with the fast pace of the game, making sure players are detected correctly in each frame.

  - **Training Details**: YOLO was trained using a custom dataset on GPU, ensuring fast and accurate detection in real-time.
  - **Result**: The model draws a box around each player that updates in real-time, making it easy to track their movements during the game.


# 2) BALL/SHUTTLE TRACKING
## Shuttlecock Tracking

- **Kalman Filtering**  
  Kalman filtering is used to smooth out the shuttlecock's trajectory and reduce false positives. It predicts the shuttlecock's position in the next frame, which helps in filtering out inaccurate detections.

- **Additional False Positive Filtering**  
  To further address false positives, we randomly selected frames from the video and ran inference to find coordinates with high shuttlecock detection frequency. These high-frequency coordinates implies shuttle is found at these points in very large numbers of frames which is practically not possible, so, were added to a blacklist, identifying them as either stationary shuttlecocks or false positives.

- **Rest State Detection**  
  We developed an algorithm to determine if the shuttlecock is at rest. For a sequence of 15 frames where the shuttlecock is detected, if the maximum distance between any two detections is below a certain threshold, we conclude the shuttlecock is stationary.

- **Individual Players' Court Detection**  
  Using net coordinates from previous analysis, we determined the court area on either side of the net.

- **Linear Interpolation**  
  To handle frames where the shuttlecock is not detected, we used linear interpolation. This technique estimates the shuttlecock’s position based on its last known position and the next detected frame.

- **Speed Analysis**  
  We calculated the shuttlecock’s speed by measuring the change in position between consecutive frames where the shuttlecock is detected. This speed is expressed in pixels per frame.

# 3) Player Tracking and Movement Analysis


- **Player Detection**  
  Players were detected using YOLO, which provides accurate bounding boxes around each player.

- **Speed Analysis**  
  The speed of the players was analyzed by measuring the distance they covered between successive frames. This involves calculating the Euclidean distance between the player’s locations in different frames.

- **Scaling Pixel-Based Distance to Real-World Distance**  
  To convert pixel-based distances to real-world measurements, we used the standard dimensions of a badminton court:
  - Length: 13.41 meters
  - Width: 6.1 meters

  By knowing these dimensions, we can calculate the distance in pixels between the top left and top right corners of the court (6.1 meters) and between the top left and bottom left corners (13.41 meters). This allows us to scale the Euclidean distance between player positions from pixels to meters using a unitary method.

  For more detailed scaling methods, we referred to the research paper from IIIT Hyderabad, "Towards Real-Time Analysis of Broadcast Badminton Videos."

- **Distance Calculation**  
  We calculate the Euclidean distance between the player’s positions in successive frames to determine the distance covered in pixels. This pixel-based distance is then scaled into meters using the court dimensions, providing actual distance values for player movement analysis.


# 4) EVENTS DETECTION


- **Shuttlecock Rest Detection**  
  We developed an algorithm to identify when the moving shuttlecock comes to rest. For a sequence of 15 frames where the shuttlecock is detected, if the maximum distance between any two detections is below a certain threshold, we conclude that the shuttlecock is stationary.

- **Score Calculation**  
  When the shuttlecock comes to rest, we check if it is within the court boundaries. If it is, we determine which player's court it is in and increment the scores accordingly. This ensures that points are accurately recorded based on the shuttlecock's final position when it stops.

- **Relay Detection and Display**  
  We track the active relay time in terms of the number of frames. Relay detection starts when:
  - In Player 1's court, the shuttlecock’s y-coordinate is consistently increasing.
  - In Player 2's court, the shuttlecock’s y-coordinate is consistently decreasing.
  
  The relay time stops when the shuttlecock comes to rest. We record the number of relays and the duration of each relay period to provide detailed insights into the game’s dynamics.

# 5) REAL-TIME COMMENTARY GENERATION

- **Commentary Generation**  
  As any player scores a point, the system sends a request to groq(a cloud-based AI using llama3-8b-8192) to generate real-time commentary. The commentary is based on the points scored. This feature enhances the user experience by providing live updates and insights into the game.

- **Speech Output**

  Now the generated commentary is converted to speech using Google Text-to-Speech (gtts) and played using the playsound library. This feature adds an interactive element to the game analysis, making it more engaging for users.

# Limitations

1. **Court Swap Identification**:
   * **Limitation**: The model is currently unable to detect when players swap courts in badminton, leading to inaccurate player tracking and potential misattribution of game events to the wrong player.
   * **Suggested Solution**: Integrating positional tracking with color-based or attire-based identification for each player could help the model distinguish between players, even after they swap sides.

2. **Score Detection in Dynamic Camera Angles**:
   * **Limitation**: The model requires 10-15 consecutive frames to accurately detect the score. If the camera angle changes before this frame threshold is met, the model fails to detect the score. Since we require some minimum number of frames to conclude that shuttle is at rest.

3. **Shuttle Detection in Frames**:
   * **Limitation**: Due to the small size and high velocity of the shuttlecock, the model struggles to detect it consistently across all frames.

4. **Service Line Detection**:
   * **Limitation**: The model is currently unable to accurately detect the service line, which is crucial for determining valid serves.
   * **Suggested Solution**: Implement line detection algorithms such as Hough Transform or deep learning-based segmentation models trained specifically for badminton courts.

5. **Complex Rule Implementation**:
   * **Limitation**: The model does not currently support the detection of complex badminton rules such as cross-court service, ensuring the server’s feet remain grounded during the serve, or detecting if the shuttle is hit more than once.
   * **Suggested Solution**: 
      * For **cross-court service detection**, we need to simultaneously track player and shuttle but due to limitation of shuttle detection model we are unable to do so.
      * For **leg detection during service**, body pose estimation models can be integrated to detect the position of the player’s legs and confirm whether they are grounded. Pose detection takes more inference time hindering realtime behaviour of our model.
