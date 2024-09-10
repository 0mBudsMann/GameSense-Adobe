# CourtDetect

`CourtDetect` is a class inside the file [CourtDetect.py](CourtDetect.py). It is designed to handle tasks related to detecting and analyzing court keypoints using a Keypoint RCNN (Region-based Convolutional Neural Network) model. The class provides functionality for processing videos, detecting court keypoints, and drawing the detected court lines.

## Class Overview

### `CourtDetect`

The `CourtDetect` class handles the following tasks:
1. **Initializing and Setting Up RCNN**: Loads the Keypoint RCNN model for court detection.
2. **Processing Video Frames**: Extracts and processes frames from a video to detect court keypoints.
3. **Detecting and Drawing Court Lines**: Uses detected keypoints to draw court lines and analyze court geometry.
4. **Player Detection**: Identifies players and their positions on the court.

### Methods

#### `__init__()`
- Initializes the class.
- Sets up the Keypoint RCNN model.
- Configures device to use CPU or GPU based on availability.

#### `reset()`
- Resets the internal state, clearing court information and detection status.

#### `setup_RCNN()`
- Loads the Keypoint RCNN model from a specified path and sets it to evaluation mode.
- Moves the model to the appropriate device (CPU/GPU).

#### `del_RCNN()`
- Deletes the loaded RCNN model from memory.

#### `pre_process(video_path, reference_path=None)`
- Opens a video file and extracts the first frame.
- Optionally loads reference court information from a JSON file.
- Detects court information from the first frame and prints the detection status.

#### `__check_court(court_info)`
- Compares detected court information with reference court information using Mean Squared Error (MSE).
- Returns `False` if the MSE exceeds a threshold (100), indicating a significant difference.

#### `get_court_info(img)`
- Processes an image to detect court keypoints using the RCNN model.
- Calculates and returns corrected court points and detection status.
- Unique: Implements a correction step to adjust detected keypoints based on expected court geometry and applies partitioning to generate detailed court points.

#### `draw_court(image, mode="auto")`
- Draws the detected court lines on an image.
- Supports two modes: "auto" (draws based on detected information) and "frame_select" (draws based on manually specified court points).

#### `__correction()`
- Corrects detected keypoints to ensure consistency with expected court geometry.
- Adjusts the y-coordinates of certain keypoints to align with the expected court layout.

#### `__partition(court_crkp)`
- Partitions the detected court keypoints to generate additional points for drawing detailed court lines.
- Splits the court into segments and interpolates additional points.

#### `player_detection(outputs)`
- Analyzes detected keypoints to identify players and their positions on the court.
- Filters detected joints based on their positions relative to the court.

#### `__top_bottom(joint)`
- Determines the top and bottom players based on their vertical position on the court.
- Swaps player positions if necessary.

#### `__check_top_bot_court(indices, boxes)`
- Checks if detected players are in the top and bottom parts of the court.
- Ensures that both top and bottom court sections have players.

#### `__check_in_court_instances(joints)`
- Identifies which detected keypoints are within the court boundaries.

#### `__in_court(joint)`
- Determines if a given keypoint (joint) is within the court boundaries based on geometric criteria.

#### `hori_lines_in_court(frame)`
- Detects horizontal lines within the court area from a frame using edge detection and Hough Line Transform.
- Merges detected lines based on y-coordinate proximity and draws them on the frame.
- Unique: Applies a shift to top and bottom corners of the detected court area to improve line detection accuracy.

## Unique Aspects

- **Correction of Keypoints**: Implements a correction step to adjust detected keypoints to align with expected court geometry.
- **Detailed Court Partitioning**: Uses partitioning and interpolation to generate additional points for detailed court line drawing.
- **Player Position Analysis**: Includes logic for detecting players' positions and distinguishing between top and bottom court sections.
- **Line Detection**: Uses advanced techniques like edge detection and Hough Line Transform to detect and merge horizontal lines in the court area.

# NetDetect

`NetDetect` is a class implemented in [NetDetect.py](NetDetect.py) for detecting and analyzing keypoints in sports net images using a Keypoint RCNN (Region-based Convolutional Neural Network). It leverages PyTorch and OpenCV to process video frames and extract net information. The class provides methods for setup, processing, and drawing net keypoints.

## Functions and Their Functioning

### `__init__(self)`

- **Purpose**: Initializes the `NetDetect` object.
- **Description**: Sets the device to CPU, initializes `normal_net_info` and `got_info` as `None` and `False`, respectively, and calls `setup_RCNN()` to configure the RCNN model.

### `reset(self)`

- **Purpose**: Resets the detected net information.
- **Description**: Clears `got_info` and `normal_net_info` to reset the state of the object.

### `setup_RCNN(self)`

- **Purpose**: Configures the RCNN model for net detection.
- **Description**: Loads the pre-trained Keypoint RCNN model weights from a specified path and sets the model to evaluation mode.

### `del_RCNN(self)`

- **Purpose**: Deletes the RCNN model from memory.
- **Description**: Removes the RCNN model from the object to free up memory.

### `pre_process(self, video_path, reference_path=None)`

- **Purpose**: Processes the first frame of a video to detect the net.
- **Description**: 
  - Opens the video file and reads the first frame.
  - Uses the `get_net_info()` method to detect the net.
  - If the net is detected, updates `normal_net_info` and returns `0`; otherwise, returns `-1`.

### `__check_net(self, net_info)`

- **Purpose**: Checks if the detected net information is consistent with the reference net.
- **Description**: 
  - Compares the newly detected net information with `normal_net_info` using Mean Squared Error (MSE).
  - If the MSE is greater than 100, returns `False`; otherwise, returns `True`.

### `get_net_info(self, img)`

- **Purpose**: Extracts net keypoints from an image.
- **Description**:
  - Converts the image to a tensor and passes it through the RCNN model.
  - Applies Non-Maximum Suppression (NMS) to filter keypoints.
  - Performs a correction and partitioning of the keypoints.
  - Checks if the detected keypoints match the reference net and returns the corrected keypoints along with a boolean indicating if the detection is successful.

### `draw_net(self, image, mode="auto")`

- **Purpose**: Draws the detected net on the image.
- **Description**:
  - If no net information is available and mode is "auto", returns the original image.
  - If `mode` is "frame_select", uses the current detected keypoints to draw the net.
  - Draws lines and keypoints on the image to represent the net.

### `__correction(self)`

- **Purpose**: Corrects the net keypoints to ensure consistent representation.
- **Description**:
  - Computes and adjusts the y-coordinates of the keypoints for the net to align properly.
  - Adjusts the x-coordinates for vertical alignment of the net points.

### `__partition(self, net_crkp)`

- **Purpose**: Partitions and organizes keypoints for visualization.
- **Description**:
  - Defines additional keypoints to form a complete representation of the net.
  - Returns the partitioned keypoints for further processing or drawing.

## Unique Aspects

- **Correction Method**: The `__correction()` method ensures that keypoints are adjusted to provide a consistent representation of the net, which is unique compared to other implementations that may not correct or align keypoints.
- **Keypoint Partitioning**: The `__partition()` method adds intermediate keypoints to better represent the net structure, which may not be common in simpler keypoint detection models.

# draw_court_and_net_on_frames

`draw_court_and_net_on_frames` is a function implemented in [om.py](../../om.py) designed to overlay court and net keypoints on video frames. It utilizes OpenCV to draw lines representing the court and net information extracted from a JSON file.

## Function and Its Functioning

### `draw_court_and_net_on_frames(frames)`

- **Purpose**: Draws court and net keypoints on a series of video frames.
- **Description**:
  - **Inputs**: 
    - `frames`: A list of frames (images) on which the court and net information will be drawn.
  - **Steps**:
    1. **Load Keypoints**: 
       - Reads court and net coordinates from `coordinates.json` located in `./result/court_and_net/courts/court_kp/`.
    2. **Convert Coordinates**:
       - Converts the loaded coordinates to NumPy arrays for easier manipulation.
    3. **Process Frames**:
       - Iterates through each frame in the `frames` list.
       - **Draw Court Lines**:
         - Draws green lines between all pairs of points in the `court_info` array, representing the court boundaries.
       - **Draw Net Lines**:
         - Draws red lines between all pairs of points in the `net_info` array, representing the net.
    4. **Return Processed Frames**:
       - Appends the modified frame to the `processed_frames` list and returns this list.

## Unique Aspects

- **Pairwise Line Drawing**: The function uses a nested loop to draw lines between all pairs of points for both court and net information. This approach ensures that all possible connections between points are visualized, which may be more comprehensive than simpler methods that only connect specific pairs.
- **Color Coding**: The use of distinct colors (green for court lines and red for net lines) helps in clearly distinguishing between the court and net information on the frames.
