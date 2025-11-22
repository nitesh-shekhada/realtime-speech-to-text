import sounddevice as sd
import numpy as np
import queue
import threading
from faster_whisper import WhisperModel

# ============================
# SETTINGS
# ============================
samplerate = 16000
block_duration = 0.5        # seconds (smaller = lower latency)
chunk_duration = 2          # seconds for each transcription window
channels = 1

frames_per_block = int(samplerate * block_duration)
frames_per_chunk = int(samplerate * chunk_duration)

audio_queue = queue.Queue()
audio_buffer = []


# ============================
# LOAD MODEL (USE GPU)
# ============================
# Best balance: medium.en, float16, CUDA
model = WhisperModel(
    "medium.en",
    device="cpu",
    compute_type="int8"
)


# ============================
# AUDIO CALLBACK (CALLED EVERY BLOCK)
# ============================
def audio_callback(indata, frames, time, status):
    if status:
        print("Status:", status)
    audio_queue.put(indata.copy())


# ============================
# RECORD AUDIO IN BACKGROUND
# ============================
def recorder():
    with sd.InputStream(
        samplerate=samplerate,
        channels=channels,
        callback=audio_callback,
        blocksize=frames_per_block
    ):
        print("🎤 Listening... Press Ctrl + C to stop.")
        while True:
            sd.sleep(100)


# ============================
# TRANSCRIBE CONTINUOUSLY
# ============================
def transcriber():
    global audio_buffer

    while True:
        block = audio_queue.get()
        audio_buffer.append(block)

        total_frames = sum(len(b) for b in audio_buffer)

        if total_frames >= frames_per_chunk:
            # Combine all blocks into one chunk
            audio_data = np.concatenate(audio_buffer)[:frames_per_chunk]
            audio_buffer = []  # clear buffer

            # Flatten to float32
            audio_data = audio_data.flatten().astype(np.float32)

            # Transcribe
            segments, _ = model.transcribe(
                audio_data,
                language="en",
                beam_size=1
            )

            # Print the partial transcription
            for seg in segments:
                print(">>", seg.text.strip())


# ============================
# START THREADS
# ============================
threading.Thread(target=recorder, daemon=True).start()
transcriber()
