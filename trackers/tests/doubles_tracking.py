import json
import os
from ultralytics import YOLO
import cv2
import pickle as pkl

class Doubles_Tracking:
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
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            output_frames.append(frame)

        return output_frames