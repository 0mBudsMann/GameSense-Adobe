import cv2
import copy
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from torchvision.transforms import transforms
from torchvision.transforms import functional as F
import os
from src.tools.utils import write_json, clear_file, is_video_detect, find_next, find_reference

from src.models.CourtDetect import CourtDetect
from src.models.NetDetect import NetDetect
import argparse

import logging
import traceback
import warnings

# Clear the polyfit RankWarning
warnings.simplefilter('ignore', np.RankWarning)

parser = argparse.ArgumentParser(description='para transfer')
parser.add_argument('--folder_path',
                    type=str,
                    default="videos",
                    help='folder_path -> str type.')
parser.add_argument('--result_path',
                    type=str,
                    default="res",
                    help='result_path -> str type.')
parser.add_argument('--force',
                    action='store_true',
                    default=False,
                    help='force -> bool type.')

args = parser.parse_args()
print(args)

folder_path = args.folder_path
force = args.force
result_path = args.result_path

for root, dirs, files in os.walk(folder_path):
    for file in files:
        _, ext = os.path.splitext(file)
        if ext.lower() in ['.mp4']:
            video_path = os.path.join(root, file)
            print(video_path)
            video_name = os.path.basename(video_path).split('.')[0]

            if is_video_detect(video_name):
                if force:
                    clear_file(video_name)
                else:
                    continue

            full_video_path = os.path.join(f"{result_path}/videos", video_name)
            if not os.path.exists(full_video_path):
                os.makedirs(full_video_path)

            # Open the video file
            video = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
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
                continue

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

            write_json(court_dict, video_name,
                       f"{result_path}/courts/court_kp", "w")

            # Release the video capture object after processing the first frame
            video.release()

            try:
                # Code block that may raise exceptions
                print("-" * 10 + "Ball Detection is not included in this version" + "-" * 10)
            except KeyboardInterrupt:
                print("Caught exception type on main.py ball_detect:",
                      type(KeyboardInterrupt).__name__)
                logging.basicConfig(filename='logs/error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
                logging.error(traceback.format_exc())
                exit()
            except Exception:
                print("Caught exception type on main.py ball_detect:",
                      type(Exception).__name__)
                logging.basicConfig(filename='logs/error.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
                logging.error(traceback.format_exc())
