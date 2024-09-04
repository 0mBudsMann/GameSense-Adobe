import json
import os
from ultralytics import YOLO
import cv2
import pickle as pkl


class ShuttleTracker:
    def __init__(self, model_path):
        self.model = YOLO(model_path)

    # Detect shuttle in multiple frames
    def detect_frames(self, frames, read_from_record=False, record_path=None):
        detect_shuttles = []

        # read the data from the pkl file if read_from_record is True
        if read_from_record and record_path is not None:
            with open(record_path, 'rb') as f:
                detected_players = pkl.load(f)
            return detected_players


        for frame in frames:
            detect_shuttles.append(self.detect_frame(frame))

        # keep the record of detected shuttle in a pkl file to reduce pre-processing
        if record_path is not None:
            os.makedirs(os.path.dirname(record_path), exist_ok=True)
            with open(record_path, 'wb+') as f:
                pkl.dump(detect_shuttles, f)

        return detect_shuttles

    # Detect shuttle in a single frame
    def detect_frame(self, frame):
        results = self.model.track(frame, persist=True)[0]
        id_name = results.names

        shuttle_dict = {}

        for box in results.boxes:
            # print(box)
            # exit(1)
            # track_id = int(box.id.tolist()[0])
            result = box.xyxy.tolist()[0]
            object_class_id = box.cls.tolist()[0]

            shuttle_dict[object_class_id] = {
                'coordinates': result,
                'class_id': object_class_id
            }

        return shuttle_dict

    # Draw boxes around detected shuttle
    def draw_boxes(self, frames, detected_shuttles):
        output_frames = []

        for frame, player_dict in zip(frames, detected_shuttles):
            for track_id, data in player_dict.items():
                result = data['coordinates']
                x1, y1, x2, y2 = map(int, result)

                box_color = (0, 0, 255)
                text_color = (36, 255, 12)
                box_thickness = 3
                text_thickness = 3
                font_scale = 1

                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, box_thickness)

                text = f"Shuttle"
                text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_thickness)
                text_w, text_h = text_size
                cv2.rectangle(frame, (x1, y1 - text_h - 10), (x1 + text_w, y1), box_color, cv2.FILLED)
                cv2.putText(frame, text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, text_color, text_thickness)

            output_frames.append(frame)

        return output_frames

    # Save shuttle data to a JSON file
    # def save_player_data(self, detected_players, file_path):
    #     os.makedirs(os.path.dirname(file_path), exist_ok=True)
    #
    #     all_data = []
    #
    #     for player_dict in detected_players:
    #         frame_data = {}
    #         for track_id, data in player_dict.items():
    #             frame_data[track_id] = data
    #         all_data.append(frame_data)
    #
    #     with open(file_path, 'w') as f:
    #         json.dump(all_data, f, indent=4)