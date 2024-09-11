# GameSense-Adobe

## Introduction
The **Badminton Game Analyzer** is a comprehensive software solution designed for real-time analysis of badminton games using cutting-edge computer vision algorithms and machine learning techniques. The system focuses on accurately detecting players, court boundaries, and the net, while also tracking the shuttlecock's movement to provide a detailed analysis of gameplay. In addition, it automates scoring based on player actions and game events, leveraging Region-based Convolutional Neural Networks (RCNN) and a custom-trained YOLOv8m model.

## For understanding working and flow of our model read [main_function.md](main_function.md)
## Model Weights Download Instructions

Due to the large size of the model weights files, we have hosted them on cloud services. Please follow the instructions below to download and place the weights in the correct directories.

### 1. Weights for Court and Net Detection

Download the weights files from the following link: [Court and Net Detection Weights](https://mega.nz/folder/upVAFDzD#McZgcaED3fe7XTtxdkvxjA)

**Instructions:**

1. Download `court_kpRCNN.pth` and `net_kpRCNN.pth`.
2. Place them in the directory `models/court_and_net_detection/src/models/weights`.

### 2. Weights for Single Player Detection

Download the weights file from the following link: [Single Player Detection Weight](https://mega.nz/file/SgNFzSJK#2cWSOMqG3VM5beTuapqiSLDiIM5Q7ZgoyB34SqKtvFA) in `models/player_detection/weights/only_player`

### 3. Weights for Doubles Player Detection

```bash
   cd models/player_detection/weights/doubles

   wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8m.pt
```

### 4. Weights for Shuttle Detection

- Download the weights file from the following link: [Shuttle Detection Weight](https://drive.google.com/file/d/1wT6zbOz8UsEG0yizwUnJ3kLedQdIhfZg/view)

- Place `best.pt` in the directory `models/shuttle_detection/weights`.


## Features
- **Player Detection**: Utilizes advanced object detection models to track player positions in real-time.
- **Court and Net Detection**: Accurately identifies court boundaries and the net to define gameplay areas.
- **Shuttle Analysis**: Tracks shuttlecock trajectory, speed, and placement to provide insights into gameplay strategy.
- **Automated Scoring**: Automatically updates scores based on real-time events such as shuttle hits and misses.
- **Real-time Tracking**: Implements a YOLOv8m-based detection pipeline optimized for detecting fast-moving objects like the shuttlecock.
- **Custom-trained Models**: Both RCNN and YOLOv8m models are custom-trained to enhance the precision of detection specific to badminton gameplay.
- **Speed and Distance Estimation**: Estimates shuttlecock speed and distance traveled to analyze player performance and game dynamics.
- **Kalman Filtering**: Implements Kalman filtering to improve shuttlecock tracking accuracy and reduce noise in the trajectory estimation.
- **Doubles Match Support**: Supports tracking and analysis of doubles badminton matches, including player positions and shuttlecock movements.
- **Commentary Integration**: Provides a user-friendly interface for generating commentary based on real-time game analysis.

## Technical Stack
- **YOLOv8m**: Custom-trained for real-time player, shuttlecock, court, and net detection.
- **RCNN (Region-based Convolutional Neural Networks)**: Used for detailed shuttle and scoring analysis.
- **OpenCV**: Employed for video frame extraction, image processing, and visualization.
- **TensorFlow/PyTorch**: For training and fine-tuning machine learning models.
- **NVIDIA CUDA**: Accelerates real-time inference using GPU processing.

## Folder Structure
```
|-- models/
    |-- commentary/
        |-- commentary.ipynb (Jupyter Notebook for generating commentary)
    |-- court_and_net_detection/ (Contains all the rcnn model files for court and net detection)
    |-- player_detection/ (Contains all the yolo model files for player detection)
    |-- shuttle_detection/ (Contains all the yolo model files for shuttle detection (First Approach))
    |-- shuttle_detection_kalman/ (Contains all the yolo model files along kalman filter for shuttle detection (Second Approach))  
|
|-- record/                  
    |-- player_detections.pkl (contains the player buffer for already inferenced video)  
    |-- shuttle_detections.pkl 
|
|-- result/                    
    |-- court_and_net (has json files for court and net detection)
    |-- player_data (has json files for player detection)
    |-- shuttle_data (has json files for shuttle detection)
|
|-- speed_distance_estimator/                   
    |-- __init__.py
    |-- speed_n_distance.py (speed and distance estimator for both doubles and singles match)
|
|-- trackers/
    |-- tests (for testing purposes)
    |-- __init__.py
    |-- player_tracker.py (player tracker for tracking players)
    |-- doubles_tracking.py (doubles tracking for tracking players)
    |-- shuttle_tracker.py (shuttle tracker for tracking shuttle (First Approach))
    |-- shuttle_tracker_2.py (shuttle tracker for tracking shuttle (Second Approach))
    |-- kalman_filter_tracker.py
    |-- kalman_filter_tracker_2.py (contains all the rules for the game and the kalman filter for shuttle tracking (Implemented))
|
|-- commentary/
    |-- __init__.py
    |-- groq_config.py (config file for sending a prompt request to groq using llama3-8b-8192 for generating commentary)
    |-- speech.py (contains all the functions for text to speech conversion using gtts and playsound)
|-- Trash/ (code no longer in use)
|      
|-- utils/
    |-- __init__.py
    |-- box_utils.py (contains all the utility functions for box)
    |-- video_utils.py (contains all the utility functions for video)
    |-- links.txt (contains all the links for the the testing footages)
|
|-- main.py (main file for running the code)
|-- requirements.txt (contains all the dependencies)
|-- README.md
```

## Usage
1. Clone the repository:
   ```bash
   git clone https://github.com/0mBudsMann/GameSense-Adobe.git
   cd GameSense-Adobe
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the analysis:
   For Singles match video
   ```bash
   python3 main.py --video_path path_to_video
   ```
   
    For Doubles match video
    ```bash
    python3 main.py -doubles --video_path path_to_video
   ```
   
    For loading data from buffer
    ```bash
    python3 main.py --video_path path_to_video --buffer
    ```
   can be used with -doubles
4. For displaying output and generating realtime Speech/Commentary for the video
   ```bash
   python3 main.py --video_path path_to_video -speech
   ```

## Model Training
1. Player Detection
   - The YOLOv8m model for player detection is trained on a custom dataset of Singles badminton players.
   - The dataset consists of annotated images of players in various poses and positions on the court. link to the dataset is [here](https://universe.roboflow.com/khangnguyen/badminton-player-object-detection)
   - The model is trained using PyTorch and fine-tuned to improve detection accuracy.

2. Shuttle Detection
    - Two YOLOv8m models are trained for shuttle detection: one without a Kalman filter and one with a Kalman filter.
    - The models are trained on a dataset of shuttlecock images captured from badminton games. link to the dataset is [here](https://universe.roboflow.com/mathieu-cartron/shuttlecock-cqzy3/dataset/1)
    - The models are trained using PyTorch and optimized for real-time inference.

3. Court and Net Detection
    - The RCNN model for court and net detection is trained on a custom dataset of badminton court and net images.
    - The dataset includes annotated images of badminton courts and nets from various angles and lighting conditions.
    - The model is trained using TensorFlow and fine-tuned to accurately detect court boundaries and the net.

We used our college GPU's for training the models. (RTX 4090 24 GB)

## Contributors
- [Jarviss77](https://github.com/Jarviss77)
- [OmBudsMann](https://github.com/0mBudsMann)
- [breakthe-rule](https://github.com/breakthe-rule)
