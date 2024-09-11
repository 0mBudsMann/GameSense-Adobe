# 1) GAME SELECTION AND PLAYER AREA MARKING

## Game Chosen: Badminton

- **Why We Chose Badminton Over TT and Tennis**  
  We chose badminton because it offers the right mix of challenges for real-time detection. The game has a medium-sized court and fast gameplay, making it perfect for testing our detection models. TT has quick movements in a small area, while tennis covers a large area but moves more slowly. Badminton strikes a balance, with complex player movements and shuttlecock trajectories, making it an ideal choice. It’s also a popular sport with a growing need for automated analysis tools in training and match reviews.

## Net and Court Detection

- **Model Selection: RCNN vs. YOLO**  
  For detecting the net and court, we considered two popular models: YOLO and RCNN. YOLO is known for its speed, which is great for real-time tasks, but **accuracy was our top priority** since all further analysis relies on getting this part right. Because we only needed to detect the net and court in one frame, time wasn’t a big concern, so we chose RCNN. RCNN is known for its **robustness**, meaning it’s excellent at accurately detecting objects, even under different conditions like lighting and angles.

## Player Detection

- **YOLO Implementation**  
  For detecting players, we used YOLO because it’s fast, which is crucial for real-time analysis. We trained YOLO on a powerful NVIDIA 4090 GPU (courtesy of one of our professors for lending us the GPU), allowing us to handle large datasets quickly. YOLO’s speed ensures we can keep up with the fast pace of the game, making sure players are detected correctly in each frame.

  - **Training Details**: YOLO was trained using a custom dataset on GPU, ensuring fast and accurate detection in real-time.
  - **Result**: The model draws a box around each player that updates in real-time, making it easy to track their movements during the game.

# 2) SHUTTLECOCK TRACKING

## Shuttlecock Tracking

- **Kalman Filtering**  
  Kalman filtering is used to smooth out the shuttlecock's trajectory and reduce false positives. It predicts the shuttlecock's position in the next frame, which helps in filtering out inaccurate detections.

- **Additional False Positive Filtering**  
  To further address false positives, we randomly selected frames from the video and ran inference to find coordinates with high shuttlecock detection frequency. These high-frequency coordinates imply the shuttle is found at these points in a very large number of frames, which is practically not possible, so these were added to a blacklist, identifying them as either stationary shuttlecocks or false positives.

- **Rest State Detection**  
  We developed an algorithm to determine if the shuttlecock is at rest. For a sequence of 15 frames where the shuttlecock is detected, if the maximum distance between any two detections is below a certain threshold, we conclude the shuttlecock is stationary.

- **Individual Players' Court Detection**  
  Using net coordinates from previous analysis, we determined the court area on either side of the net.

- **Linear Interpolation**  
  To handle frames where the shuttlecock is not detected, we used linear interpolation. This technique estimates the shuttlecock’s position based on its last known position and the next detected frame.

- **Speed Analysis**  
  We calculated the shuttlecock’s speed by measuring the change in position between consecutive frames where the shuttlecock is detected. This speed is expressed in pixels per frame.

# 3) PLAYER TRACKING AND MOVEMENT ANALYSIS

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

- **Net Touch Event Detection**  
  We introduced an additional event to detect when the shuttlecock touches the net during play. Since we already have the net coordinates from previous analyses, we compare the shuttlecock’s position with the net. If the shuttlecock’s y-coordinate falls within a small threshold near the net’s y-coordinate, we register a net touch event. This provides critical information for identifying faults or disruptions during rallies.

- **Relay Detection and Display**  
  We track the active relay time in terms of the number of frames. Relay detection starts when:
  - In Player 1's court, the shuttlecock’s y-coordinate is consistently increasing.
  - In Player 2's court, the shuttlecock’s y-coordinate is consistently decreasing.

  The relay time stops when the shuttlecock comes to rest. We record the number of relays and the duration of each relay period to provide detailed insights into the game’s dynamics.

- **Shuttlecock Speed Detection**  
  To enhance the analysis, we also implemented speed detection for the shuttlecock. By measuring the change in its position between consecutive frames, we calculate the speed in pixels per frame. This value is then scaled to real-world units using the court’s dimensions, providing the shuttlecock’s speed in meters per second. This allows us to track how fast the shuttlecock is moving, which is essential for understanding player reaction times and shuttlecock dynamics during a match.

# 5) SCORING AND METRICS
- **Score Calculation**  
  When the shuttlecock comes to rest, we check if it is within the court boundaries. If it is, we determine which player's court it is in and increment the scores accordingly. This ensures that points are accurately recorded based on the shuttlecock's final position when it stops.


# 6) ACCURACY

We have attached a [MEGA link](https://mega.nz/folder/a9UUSYgD#U5cDKoQ-X-qfaXyBDOPsNQ) containing different test cases and their corresponding outputs.

**Please note that for the Adobe test case, we provided two outputs. The original test case had low-quality video, which led to net detection failure. To address this, we recorded the same video from YouTube in higher quality. As you can see in the second output, net detection works flawlessly in the better-quality video.**

This demonstrates the importance of video quality in the accuracy of our system, but also shows how our model performs robustly under optimal conditions.

# 7) REAL-TIME PROCESSING

- **Threading for Speed Optimization**  
  We implemented threading to handle independent tasks like shuttlecock tracking, player detection, and event analysis concurrently. This speeds up processing by running multiple operations in parallel, ensuring the system can analyze frames in real-time.

- **Immediate Scoring and Relay Updates**  
  As soon as the frame where the shuttlecock comes to rest is processed, the system instantly determines whether a score has been made, which player’s court the shuttlecock is in, and updates the score accordingly. Relay information, including active relay time, is also updated as soon as the frame is processed, allowing for immediate feedback and continuous real-time tracking.

- **YOLO for Fast Detection**  
  YOLO was used for both shuttlecock and player detection due to its speed and efficiency. Its ability to rapidly process each frame ensures that we can detect player movements and shuttlecock positions in near real-time, essential for fast-paced sports like badminton.

- **Efficient Resource Utilization**  
  With threading and YOLO’s fast detection capabilities, we optimized the system to be both resource-efficient and responsive, ensuring smooth and fast real-time analysis of scoring, player movement, and relay dynamics.

- **Minimizing Latency**  
  Through efficient task management and the use of high-performance algorithms, we minimized latency, ensuring that all detections, calculations, and updates—such as scoring and relay time—are delivered in real-time, providing instant feedback during live game analysis.

# 8) ROBUSTNESS

We have detailed all the algorithms used in this project, including YOLO for fast detection, RCNN for accurate detection, Kalman filtering to remove false positives, and custom algorithms for shuttlecock rest detection, scoring, and relay tracking. These methods ensure high accuracy and reliability, making the system robust for real-time badminton analysis. Many algorithms have been mentioned earlier, and the fact that both accuracy and real-time processing go together in sync is what makes the algorithms used robust.

# 9) PLAYER MOVEMENT MATRIX

To analyze player movement, we calculated the Euclidean distance between the players' positions across successive frames. Using the standard dimensions of the badminton court (13.41 meters length, 6.1 meters width), we scaled the pixel-based distances into real-world meters. This allowed us to create a movement matrix, showing the distances players covered during the game.

For scaling and accuracy, we referred to the research paper from IIIT Hyderabad, "Towards Real-Time Analysis of Broadcast Badminton Videos." The matrix provides valuable insights into player movement patterns, helping track speed and distance throughout the match.

# 10) ADVANCED AI MATRIX

We implemented an **Advanced AI Matrix** for real-time commentary generation. When a player scores a point, the system communicates with **Groq**, a cloud-based AI leveraging **LLaMA3-8b-8192**, to instantly generate context-aware commentary. This advanced AI matrix enhances the overall experience by delivering live, intelligent insights based on in-game events, adding a sophisticated layer of interaction and engagement during the match.
- **Shuttlecock tracing**  

The system continuously tracks the shuttlecock’s movement across the court using a combination of YOLO-based object detection and linear interpolation for real-time precision. By tracking the shuttlecock’s x and y coordinates in each frame, we monitor its trajectory to determine important game events such as shots, relays, and rests. This tracing allows us to analyze the gameplay in greater depth, enabling accurate event detection and commentary.

- **Shuttlecock Speed Detection**

To further enhance gameplay analysis, we implemented **Shuttlecock Speed Detection**. The system calculates speed by measuring the change in the shuttlecock's position between consecutive frames. This speed, initially computed in pixels per frame, is converted into real-world units (meters per second) using the known dimensions of the badminton court. Tracking the shuttlecock's speed offers insights into player responses and shot power, adding a new layer of data for real-time commentary and post-game analysis.
# 11) REAL-TIME COMMENTARY GENERATION (BONUS)

- **Commentary Generation**  
  As any player scores a point, the system sends a request to groq(a cloud-based AI using llama3-8b-8192) to generate real-time commentary. The commentary is based on the points scored. This feature enhances the user experience by providing live updates and insights into the game.

- **Speech Output**

  Now the generated commentary is converted to speech using Google Text-to-Speech (gtts) and played using the playsound library. This feature adds an interactive element to the game analysis, making it more engaging for users.


# 12) DOUBLES (BONUS)

For doubles matches, we utilized YOLO dataset for detecting multiple players on the court. Please note this is different from dataset we used for single person detection. This ensures that both players from each team are accurately tracked and analyzed in real-time, maintaining the same level of precision used in singles matches.

We have provided a test case for doubles in the output, showcasing the system’s ability to handle multiple players simultaneously. This demonstrates the robustness of our player detection and tracking algorithms, even in more complex scenarios like doubles games. Our system seamlessly adapts to the increased complexity of movement and interaction between four players.



