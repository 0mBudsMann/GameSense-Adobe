from doubles_tracking import Doubles_Tracking
import cv2

def read_video(video_path):
    cap = cv2.VideoCapture(video_path, cv2.CAP_FFMPEG)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

def write_video(frames, output_path, fps):
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    for frame in frames:
        video_writer.write(frame)
    video_writer.release()

def main():
    doubles_tracking = Doubles_Tracking('yolov8m.pt')

    input_video = '../../utils/footages/doubles.mp4'

    frames = read_video(input_video)

    detected_players = doubles_tracking.detect_frames(frames, read_from_record=False, record_path="record/player_detections.pkl")

    output_frames = doubles_tracking.draw_boxes(frames, detected_players)

    write_video(output_frames, 'output.mp4', 60)
if __name__ == '__main__':
    main()

