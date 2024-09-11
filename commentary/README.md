# Commentary

For code refer [speech.py](speech.py)
## Features

- **Real-time video processing**: Continuously captures and displays video frames from a video source.
- **Score detection**: Monitors score changes by comparing current and previous scores.
- **Dynamic commentary generation**: Uses an AI language model to generate context-aware commentary.
- **Text-to-speech conversion**: Converts the generated commentary into speech.
- **Audio playback**: Plays the audio commentary while the video is being displayed.
- **Multithreading**: Utilizes multithreading to handle video display and audio generation/playback simultaneously.

## Function Descriptions

### `generate_and_play_commentary(commentary_text)`

- **Purpose**: Generates dynamic commentary text using an AI model and plays it back as audio.
- **Uniqueness**: Integrates AI-generated content with text-to-speech conversion and audio playback in real-time.
- **Process**:
  - Calls `generate_commentary()` to get a customized commentary message.
  - Uses `gTTS` to convert the text to speech.
  - Speeds up the audio playback for a more lively commentary using `pydub`.
  - Plays the audio without blocking the main video display thread.

### `display_and_generate_commentary(video_source)`

- **Purpose**: Captures video frames from a given source and displays them while checking for score changes.
- **Uniqueness**: Manages real-time video capture and display, ensuring smooth playback while integrating other real-time functionalities.
- **Process**:
  - Opens the video source using OpenCV.
  - Reads frames in a loop and updates the `current_frame`.
  - Calls `detect_score_change()` to monitor for any score updates.
  - Displays the video frame using OpenCV's GUI functions.
  - Handles graceful shutdown on user input.

### `detect_score_change(frame)`

- **Purpose**: Detects changes in the score and triggers commentary generation when a change is detected.
- **Uniqueness**: Synchronizes score monitoring with real-time video frames to ensure timely commentary.
- **Process**:
  - Determines the frame number and retrieves the corresponding score from pre-loaded data.
  - Compares the current score with the last known score.
  - If a player's score has increased, initiates a new thread to generate and play commentary.
  - Updates `last_score` to the current score.

### `generate_commentary(message)`

- **Purpose**: Generates a dynamic commentary message using an AI language model via the Groq API.
- **Uniqueness**: Leverages a powerful language model to produce contextually relevant and engaging commentary.
- **Process**:
  - Sends a request to the Groq API with the given message and specified parameters.
  - Receives and returns the AI-generated commentary text.

## Real-time Behavior Handling

The system is designed to handle real-time video processing and audio playback efficiently:

- **Multithreading**: Uses threads to separate video processing from audio generation and playback, ensuring that the video display remains smooth and responsive.
- **Frame Locking**: Implements a frame lock (`frame_lock`) to synchronize access to the `current_frame`, preventing race conditions in a multithreaded environment.
- **Asynchronous Audio Generation**: Generates and plays audio commentary in separate threads to avoid blocking the main video loop.
- **Efficient Resource Management**: Releases video capture resources and destroys GUI windows upon exit to free up system resources.
