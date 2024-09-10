import cv2
import threading
import time
from gtts import gTTS
import io
from pydub import AudioSegment
from pydub.playback import play
import json

frame_lock = threading.Lock()
current_frame = None

with open('result/scoring/score.json', 'r') as f:
    data = json.load(f)


def generate_and_play_commentary(commentary_text):
    tts = gTTS(text=commentary_text, lang='en')
    with io.BytesIO() as audio_buffer:
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_segment = AudioSegment.from_mp3(audio_buffer)
        play(audio_segment)

def display_and_generate_commentary(video_source):
    cap = cv2.VideoCapture(video_source)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        with frame_lock:
            global current_frame
            current_frame = frame

        shuttle_scored = detect_shuttle(frame)

        if shuttle_scored:
            commentary_text = "Great shot! A point for the player!"
            threading.Thread(target=generate_and_play_commentary, args=(commentary_text,)).start()

        cv2.imshow('Badminton Match', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def detect_shuttle(frame):
    return time.time() % 7 < 0.1