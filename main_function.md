# Badminton Game Analyzer

Welcome to the **Badminton Game Analyzer**! This software provides real-time analysis of badminton games, leveraging advanced computer vision and machine learning techniques to offer detailed insights into gameplay. Whether you're analyzing singles or doubles matches, this tool helps in tracking players, detecting court boundaries and the net, and providing automated scoring based on player actions and game events.

## User-Made Functions

The **Badminton Game Analyzer** utilizes several user-defined functions and classes to perform its analysis:

- **`PlayerTracker`**: Handles player detection and tracking in singles matches. This class identifies players, tracks their movements, and captures data on their positions and actions throughout the match.

    For more information on the `PlayerTracker`, refer to the [PlayerTracker](trackers/README.md/#playertracker)

- **`Doubles_Tracking`**: Similar to `PlayerTracker`, but tailored for doubles matches. It manages the tracking of all four players, providing insights into their movements, positions, and interactions on the court.

    For more information on the `Doubles_Tracking`, refer to the [Doubles_Tracking](trackers/README.md/#doubles_tracking)

- **`real_time_detection_and_tracking`**: Manages the detection and tracking of the shuttlecock, updates the match score, tracks penalties, and generates real-time commentary. It processes video frames in real-time to accurately annotate shuttlecock positions, match events, and provide live commentary on the game's progress.

    For more information on the `real_time_detection_and_tracking`, refer to the [real_time_detection_and_tracking](trackers/README.md/#real_time_detection_and_tracking)

- **`CourtDetect`**: Detects and visualizes court boundaries. This class processes video frames to identify the edges and boundaries of the court, which are essential for accurate game analysis.

    For more information on the `CourtDetect`, refer to the [CourtDetect](models/court_and_net_detection/src/models/README.md/#courtdetect)

- **`NetDetect`**: Identifies the net within the video frames. It works in conjunction with `CourtDetect` to provide a complete view of the court setup.

    For more information on the `NetDetect`, refer to the [NetDetect](models/court_and_net_detection/src/models/README.md/#netdetect)

- **`draw_court_and_net_on_frames`**: Annotates the frames with detected court boundaries and the net. This function ensures that the visual representation of the court and net is clear and accurate in the final output.

    For more information on the `draw_court_and_net_on_frames`, refer to the [draw_court_and_net_on_frames](models/court_and_net_detection/src/models/README.md/#draw_court_and_net_on_frames)

- **`SpeedAndDistance_Estimator`**: Calculates and annotates the speed and distance traveled by players. This class provides valuable metrics on player performance and movement throughout the game.

    For more information on the `SpeedAndDistance_Estimator`, refer to the [SpeedAndDistance_Estimator](speed_distance_estimator\README.md/#speedanddistance_estimator)

## Features

- **Player Detection & Tracking**: Identifies and tracks players in both singles and doubles matches.
- **Shuttlecock Tracking**: Monitors the shuttlecock's movement and provides smooth tracking paths.
- **Court & Net Detection**: Accurately detects and visualizes court boundaries and the net.
- **Speed & Distance Estimation**: Calculates and annotates the speed and distance traveled by players.
- **Automated Scoring**: Automatically updates the match score and tracks penalties.

## Getting Started

### Usage

You can run the Badminton Game Analyzer from the command line with the following arguments:

- `--video_path`: Path to the input video (required).
- `-doubles`: Use this flag if you want to enable doubles tracking (optional).
- `--buffer`: Load data from buffer rather than performing inference again (optional).

Here's an example command to run the analyzer:

```bash
python main.py --video_path path/to/your/video.mp4 -doubles
```

### How It Works

1. **Frame Extraction**: The video is processed to extract individual frames.

2. **Speed & Distance Estimation**: An object of `SpeedAndDistance_Estimator` is created to estimate the speed and distance traveled by players.

3. **Court & Net Detection**: The first frame is used to detect and plot the court boundaries and net.

4. **Player Tracking**: Depending on whether doubles tracking is enabled, the appropriate tracking class (`PlayerTracker` or `Doubles_Tracking`) is used to detect players, their positions, speed, and distance. This data is saved in a JSON file.

5. **Shuttlecock Detection**:
   - **Initial Detection Issues**: The shuttlecock detection model initially faced issues with falsely detecting the shuttlecock at various stationary points in the frame, including positions outside the court such as in the audience.
   - **Stationary Point Identification**: To address this, the first 5 seconds of the video are processed to identify stationary points where the model frequently misidentifies the shuttlecock. These points are located by finding coordinates within a 20-pixel range with high frequency of detection.
   - **Blacklisting Stationary Points**: Once these stationary points are identified, they are added to a blacklist. This blacklist helps in ignoring these points during actual shuttlecock detection to reduce false positives.
   - **Final Shuttlecock Detection**: The actual shuttlecock detection is then performed with the blacklist applied. The system identifies and annotates the shuttlecock's position in the video frames, generates real-time commentary, and updates the match score and penalties as needed.

6. **Data Annotation**: Player data, speed, and distance are annotated in the video.

7. **Interpolation**: The shuttlecock's tracking path is smoothed using `interpolate_shuttle_tracking` to provide a more visually accurate representation.

8. **Output Video**: All annotated frames are compiled into a final video with the same FPS as the input.