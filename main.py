from utils import (read_video, write_video)
from trackers import (PlayerTracker)
import argparse

def main():
    parser = argparse.ArgumentParser(description="A script that uses --buffer option")
    parser.add_argument("--buffer", action='store_true', help="load data from buffer rather than inferencing again")

    args = parser.parse_args()

    read_from_record = args.buffer

    # Read Video
    input_video = "utils/footages/short.mp4"
    frames = read_video(input_video)
    output_video = "output.mp4"

    # Inference and Tracking
    track_players = PlayerTracker("models/player_detection/weights/only_player/best.pt")
    detected_players = track_players.detect_frames(frames, read_from_record, record_path="record/player_detections.pkl")

    # Save Player Data
    track_players.save_player_data( detected_players, "result/player_data/player_data.json")

    # Draw Boxes
    output_frames = track_players.draw_boxes(frames, detected_players)

    write_video(output_frames, output_video, 60)

if __name__ == "__main__":
    main()