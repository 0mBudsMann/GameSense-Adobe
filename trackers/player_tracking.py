import json
import os
from ultralytics import YOLO
import cv2
import pickle as pkl


class PlayerTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    # Detect players in multiple frames
    def detect_frames(self, frames, read_from_record=False, record_path=None):
        detected_players = []

        # read the data from the pkl file if read_from_record is True
        if read_from_record and record_path is not None:
            with open(record_path, 'rb') as f:
                detected_players = pkl.load(f)
            return detected_players


        for frame in frames:
            detected_players.append(self.detect_frame(frame))

        # keep the record of detected players in a pkl file to reduce pre-processing
        if record_path is not None:
            os.makedirs(os.path.dirname(record_path), exist_ok=True)
            with open(record_path, 'wb+') as f:
                pkl.dump(detected_players, f)

        return detected_players

    # Detect players in a single frame
    def detect_frame(self, frame):
        results = self.model.track(frame, persist=True)[0]
        id_name = results.names

        player_dict = {}

        for box in results.boxes:
            track_id = int(box.id.tolist()[0])
            result = box.xyxy.tolist()[0]
            object_class_id = box.cls.tolist()[0]

            player_dict[track_id] = {
                'coordinates': result,
                'class_id': object_class_id
            }

        return player_dict

    # Draw boxes around detected players
    def draw_boxes(self, frames, detected_players):
        output_frames = []

        for frame, player_dict in zip(frames, detected_players):
            for track_id, data in player_dict.items():
                result = data['coordinates']
                x1, y1, x2, y2 = map(int, result)

                box_color = (0, 0, 255)
                text_color = (36, 255, 12)
                box_thickness = 3
                text_thickness = 3
                font_scale = 1

                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, box_thickness)

                text = f"Player {track_id}"
                text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_thickness)
                text_w, text_h = text_size
                cv2.rectangle(frame, (x1, y1 - text_h - 10), (x1 + text_w, y1), box_color, cv2.FILLED)
                cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, text_thickness)

            output_frames.append(frame)

        return output_frames

    # Save player data to a JSON file
    def save_player_data(self, detected_players, file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        all_data = []

        for player_dict in detected_players:
            frame_data = {}
            for track_id, data in player_dict.items():
                frame_data[track_id] = data
            all_data.append(frame_data)

        with open(file_path, 'w') as f:
            json.dump(all_data, f, indent=4)