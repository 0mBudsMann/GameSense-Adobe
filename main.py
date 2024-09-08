from utils import (read_video, write_video)
from trackers import (PlayerTracker, ShuttleTracker, real_time_detection_and_tracking, draw_shuttle_predictions, interpolate_shuttle_tracking)
import argparse
import cv2
import copy
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from torchvision.transforms import transforms
from torchvision.transforms import functional as F
import os
from models.court_and_net_detection.src.tools.utils import write_json, clear_file, is_video_detect, find_reference

from models.court_and_net_detection.src.models.CourtDetect import CourtDetect
from models.court_and_net_detection.src.models.NetDetect import NetDetect
from models.court_and_net_detection.om import draw_court_and_net_on_frames
import logging
import traceback
import warnings

from speed_distance_estimator import SpeedAndDistance_Estimator


def main():
    parser = argparse.ArgumentParser(description="A script for court and player tracking")
    parser.add_argument("--buffer", action='store_true', help="load data from buffer rather than inferencing again")
    # parser.add_argument("--video_path", type=str, required=True, help="Path to the input video")

    args = parser.parse_args()

    read_from_record = args.buffer
    # input_video = args.video_path  # Get video from the user
    input_video = 'utils/footages/short_shuttle.mp4'

    # Read Video
    frames = read_video(input_video)
    output_video = "output.mp4"

    # Inference and Tracking
    # Players
    track_players = PlayerTracker("models/player_detection/weights/only_player/best.pt")
    detected_players = track_players.detect_frames(frames, read_from_record, record_path="record/player_detections.pkl")

    # Interpolate Shuttle Tracking
    # shuttle_tracking_data = interpolate_shuttle_tracking(shuttle_tracking_data)
    # print(shuttle_tracking_data)

    # Detect speed and distance
    speed_and_distance_estimation = SpeedAndDistance_Estimator()
    speed_and_distance_estimation.speed_n_distance(detected_players)
    # speed_and_distance_estimation.speed_n_distance(detected_shuttle)

    # Save Player Data
    track_players.save_player_data(detected_players, "result/player_data/player_data.json")

    # Court and Net Detection
    # Clear the polyfit RankWarning
    warnings.simplefilter('ignore', np.RankWarning)

    video_name = os.path.basename(input_video).split('.')[0]
    result_path = "result/court_and_net/"

    if is_video_detect(video_name):
        print(f"Video {video_name} has already been processed. Skipping.")
        return

    full_video_path = os.path.join(f"{result_path}/videos", video_name)
    if not os.path.exists(full_video_path):
        os.makedirs(full_video_path)

    # Open the video file
    video = cv2.VideoCapture(input_video, cv2.CAP_FFMPEG)
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Write video information
    video_dict = {
        "video_name": video_name,
        "fps": fps,
        "height": height,
        "width": width,
        "total_frames": total_frames
    }
    write_json(video_dict, video_name, full_video_path)

    # Initialize detection classes
    court_detect = CourtDetect()
    net_detect = NetDetect()

    reference_path = find_reference(video_name)
    if reference_path is None:
        print("There is no reference frame! Now try to find it automatically.")
    else:
        print(f"The reference frame is {reference_path}. ")

    # Read only the first frame from the video
    ret, frame = video.read()
    if not ret:
        print("Error: Could not read the first frame.")
        video.release()
        return

    # Perform court and net detection on the first frame
    court_info, have_court = court_detect.get_court_info(frame)
    net_info, have_net = net_detect.get_net_info(frame)

    if have_court:
        normal_court_info = court_info
        begin_frame = 0  # Since we're only processing the first frame
        next_frame = 1  # Placeholder as there's no further processing
    else:
        print("No court detected in the first frame.")
        normal_court_info = None
        begin_frame = -1
        next_frame = -1

    if have_net:
        normal_net_info = net_info
    else:
        print("No net detected in the first frame.")
        normal_net_info = None

    # Correct net position if detected
    if normal_net_info is not None and normal_court_info is not None:
        normal_net_info[1][1], normal_net_info[2][1] = \
            normal_court_info[2][1], normal_court_info[3][1]

    court_dict = {
        "first_rally_frame": begin_frame,
        "next_rally_frame": next_frame,
        "court_info": normal_court_info,
        "net_info": normal_net_info,
    }

    write_json(court_dict, "coordinates", f"{result_path}/courts/court_kp", "w")

    # Release the video capture object after processing the first frame
    video.release()

    # Draw Boxes
    # ShuttleCock
    output_frames, tracking_data = real_time_detection_and_tracking(frames)
    print(output_frames[0].shape)

    # Interpolation
    tracking_data = interpolate_shuttle_tracking(tracking_data)
    print(tracking_data)

    output_frames = draw_shuttle_predictions(output_frames, tracking_data)
    print(output_frames)
    print(output_frames[0].shape)


    output_frames = track_players.draw_boxes(output_frames, detected_players)
    print(output_frames[0].shape)

    # output_frames = track_shuttle.draw_boxes(output_frames, detected_shuttle)

    output_frames = speed_and_distance_estimation.draw_speed_and_distance(output_frames, detected_players)
    print(output_frames[0].shape)
    # output_frames = speed_and_distance_estimation.draw_speed_and_distance(output_frames, detected_shuttle)

    output_frames = draw_court_and_net_on_frames(output_frames)
    print(output_frames[0].shape)
    # output_frames = draw_shuttle_predictions(output_frames, shuttle_tracking_data, rest_coords, listt)
    write_video(output_frames, output_video, 60)


if __name__ == "__main__":
    main()