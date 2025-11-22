# Realtime Speech-to-Text (faster-whisper • Python • FastAPI • WebSocket)

This repository provides a complete **end-to-end realtime speech-to-text system** built using **faster-whisper**, including:

- 🎙 **Local realtime microphone STT** (Python)
- 🌐 **FastAPI WebSocket backend** for streaming transcription
- 💻 **Browser client** sending audio via WebSocket
- ⚡ Ultra-fast inference with CPU (`int8`) or GPU

---

## **📌 Features**

- Realtime transcription with very low latency  
- Browser microphone → WebSocket → Python STT pipeline  
- Complete backend + frontend + local STT scripts  
- Uses `faster-whisper` (optimized Whisper implementation)  
- Minimal dependencies  
- Ready for deployment on VPS, Docker, or systemd  

---

## **📁 Project Structure**

```
/realtime-stt/
│
├── server/
│   └── main_ws.py            # FastAPI WebSocket backend
│
├── client/
│   └── index.html            # Browser WebSocket client
│
├── local-mic/
│   └── mic_stt.py            # Python runtime microphone STT
│
├── requirements.txt
└── README.md
```

---

# **🚀 1. Local Microphone Realtime STT**

**File:** `local-mic/mic_stt.py`

### **Run locally**

```bash
pip install -r requirements.txt
python local-mic/mic_stt.py
```

### **How it works**
- Captures microphone audio using `sounddevice`
- Buffers audio in 0.5s blocks
- Forms a 2-second chunk for transcription
- Passes it to **faster-whisper**
- Prints text in realtime:

```
>> hello world
>> this is realtime stt
```

---

# **🌐 2. FastAPI WebSocket Speech-to-Text Server**

**File:** `server/main_ws.py`

### **Start the server**

```bash
pip install -r requirements.txt
uvicorn server.main_ws:app --host 0.0.0.0 --port 8000
```

### **WebSocket endpoint**

```
ws://YOUR_SERVER_IP:8000/ws/stt
```

### **What the server does**
- Accepts WebSocket binary audio packets  
- Converts the bytes into NumPy float32  
- Runs `faster-whisper` on CPU  
- Sends back transcribed text in realtime  

---

# **💻 3. Browser Realtime Client**

**File:** `client/index.html`

### **How to use**
1. Open the file in Chrome  
2. Click **Start**  
3. Allow microphone permission  
4. Speak → see text appear live  

### **Audio flow pipeline**

```
Browser Mic → MediaRecorder → WebM chunks → WebSocket
→ FastAPI backend → faster-whisper → Back to browser
```

---

# **🔧 Configuration**

### Microphone script (`mic_stt.py`)
```python
block_duration = 0.5     # realtime responsiveness
chunk_duration = 2       # accuracy buffer
samplerate = 16000
```

### Browser client
```js
mediaRecorder.start(250);   // send every 250 ms
```

---

# **⚙️ Deployment (Ubuntu VPS)**

### Install dependencies
```bash
sudo apt update
sudo apt install ffmpeg python3-pip
pip install -r requirements.txt
```

### Run FastAPI server
```bash
uvicorn server.main_ws:app --host 0.0.0.0 --port=8000
```

### Allow port in firewall
```bash
sudo ufw allow 8000
```

### Access from client
```
ws://YOUR-SERVER-IP:8000/ws/stt
```

---

# **📈 Model Options & Performance**

| Whisper Model | Speed | Accuracy | Best For |
|--------------|--------|----------|----------|
| tiny.en      | Fastest | Medium | Low-latency realtime |
| small.en     | Fast | Good | Balanced default |
| medium.en    | Slow | High | Business quality |
| large-v3     | Slowest | Best | High-end CPU/GPU |

---

# **🧪 Tested On**

| Environment | Result |
|------------|--------|
| Chrome WebM recording | ✔ Works |
| FastAPI WebSocket | ✔ Stable |
| CPU inference (int8) | ✔ Fast |
| Local mic + Python | ✔ Verified |

---

# **📜 License**

MIT License – free for personal and commercial use.

