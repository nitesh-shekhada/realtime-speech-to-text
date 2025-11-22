import uvicorn
import numpy as np
import asyncio
import websockets
from faster_whisper import WhisperModel
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

# Load model once on startup (PRODUCTION)
model = WhisperModel("small.en", device="cpu", compute_type="int8")

@app.websocket("/ws/stt")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()

    audio_buffer = bytearray()

    try:
        while True:
            data = await ws.receive_bytes()
            audio_buffer.extend(data)

            # Convert to float32 NumPy
            audio_np = np.frombuffer(audio_buffer, dtype=np.uint8).astype(np.float32)

            # Avoid too much buffer
            if len(audio_np) > 48000:  # ~3 sec
                audio_buffer = bytearray()

            segments, _ = model.transcribe(audio_np, language="en", beam_size=1)

            for seg in segments:
                await ws.send_text(seg.text.strip())

    except WebSocketDisconnect:
        print("Client disconnected")

if __name__ == "__main__":
    uvicorn.run("main_ws:app", host="0.0.0.0", port=8000, reload=True)
