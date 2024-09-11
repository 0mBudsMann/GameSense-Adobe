import cv2
import threading
import time
from gtts import gTTS
import io
from pydub import AudioSegment
from pydub.playback import play
import json
from .groq_config import generate_commentary

frame_lock = threading.Lock()
current_frame = None

with open('result/scoring/score.json', 'r') as f:
    data = json.load(f)

last_score = {"Player 1": 0, "Player 2": 0}

def generate_and_play_commentary(commentary_text):

    message = generate_commentary(commentary_text)
    print("Commentary: ", message)

    tts = gTTS(text=message, lang='en')
    with io.BytesIO() as audio_buffer:
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        audio_segment = AudioSegment.from_mp3(audio_buffer)
        faster_audio = audio_segment.speedup(playback_speed=1.5)
        play(faster_audio)

def display_and_generate_commentary(video_source):
    cap = cv2.VideoCapture(video_source)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        with frame_lock:
            global current_frame
            current_frame = frame

        detect_score_change(frame)

        cv2.imshow('Badminton Match', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
def detect_score_change(frame):
    global last_score
    frame_number = int(time.time()) % len(data)

    current_score = data[str(frame_number)]
    player1_score = current_score["Player 1"]
    player2_score = current_score["Player 2"]

    if player1_score > last_score["Player 1"]:
        commentary_text = "Great shot! A point for Player 1!"
        threading.Thread(target=generate_and_play_commentary, args=(commentary_text,)).start()
    elif player2_score > last_score["Player 2"]:
        commentary_text = "Fantastic play! A point for Player 2!"
        threading.Thread(target=generate_and_play_commentary, args=(commentary_text,)).start()

    last_score = current_score