from utils import (read_video, write_video)
from trackers import (PlayerTracker)
import argparse
from speed_distance_estimator import SpeedAndDistance_Estimator

def main():
    parser = argparse.ArgumentParser(description="A script that uses --buffer option")
    parser.add_argument("--buffer", action='store_true', help="load data from buffer rather than inferencing again")

    args = parser.parse_args()

    read_from_record = args.buffer

    # Read Video
    input_video = "utils/footages/12sec.mp4"
    frames = read_video(input_video)
    output_video = "output.mp4"

    # Inference and Tracking
    track_players = PlayerTracker("models/player_detection/weights/only_player/best.pt")
    detected_players = track_players.detect_frames(frames, read_from_record, record_path="record/player_detections.pkl")
    print(detected_players)

    # Detect speed and distance
    speed_and_distance_estimation = SpeedAndDistance_Estimator()
    speed_and_distance_estimation.speed_n_distance(detected_players)

    # Save Player Data
    track_players.save_player_data( detected_players, "result/player_data/player_data.json")

    # Draw Boxes
    output_frames = track_players.draw_boxes(frames, detected_players)

    output_frames = speed_and_distance_estimation.draw_speed_and_distance(output_frames, detected_players)

    write_video(output_frames, output_video, 60)

if __name__ == "__main__":
    main()