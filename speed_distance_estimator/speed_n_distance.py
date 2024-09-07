import cv2
import sys

sys.path.append('../')
from utils import measure_distance , get_foot_position

class SpeedAndDistance_Estimator():
    def __init__(self):
        self.frame_window = 5
        self.frame_rate = 60

    def speed_n_distance(self, detected_players):
        # To store the total distance traveled by each player
        total_distance = {}

        number_of_frames = len(detected_players)

        for frame_num in range(0, number_of_frames, self.frame_window):
            last_frame = min(frame_num + self.frame_window, number_of_frames - 1)

            for player_id in detected_players[frame_num].keys():
                if player_id not in detected_players[last_frame]:
                    continue

                start_position = detected_players[frame_num][player_id]['coordinates']
                end_position = detected_players[last_frame][player_id]['coordinates']

                # Calculate the distance covered between the frames
                distance_covered = measure_distance(start_position, end_position)

                time_elapsed = (last_frame - frame_num)

                if time_elapsed == 0:
                    continue

                speed_pixels_per_frame = distance_covered / time_elapsed

                if player_id not in total_distance:
                    total_distance[player_id] = 0

                # Update the total distance covered by the player
                total_distance[player_id] += distance_covered

                # Update the speed and distance for each frame in the frame window
                for frame_num_batch in range(frame_num, last_frame + 1):
                    if player_id not in detected_players[frame_num_batch]:
                        continue

                    detected_players[frame_num_batch][player_id]['speed'] = speed_pixels_per_frame
                    detected_players[frame_num_batch][player_id]['distance'] = total_distance[player_id]

        return detected_players

    def draw_speed_and_distance(self, frames, detected_players):

        output_frames = []
        for frame_num, frame in enumerate(frames):
            for player_id, track_info in detected_players[frame_num].items():
                if "speed" in track_info:
                    speed = track_info.get('speed', None)
                    distance = track_info.get('distance', None)
                    if speed is None or distance is None:
                        continue

                    bbox = track_info['coordinates']
                    position = get_foot_position(bbox)
                    position = list(position)
                    position[1] += 40

                    position = tuple(map(int, position))
                    cv2.putText(frame, f"{speed:.2f} pixels/frame", position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)
                    cv2.putText(frame, f"{distance:.2f} pixels", (position[0], position[1] + 20), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 0, 0), 2)
            output_frames.append(frame)

        return output_frames