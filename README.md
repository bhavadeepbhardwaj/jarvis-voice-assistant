# 🎙️ Jarvis — Voice-Controlled Desktop Assistant

A local, privacy-friendly voice assistant for macOS. Jarvis listens to a spoken
command, transcribes it on-device with Whisper, routes it through a FastAPI
backend, performs a desktop action (organize files, find a file, open the news,
tell the time), and speaks the result back.

No cloud speech services — transcription runs locally via `faster-whisper`, and
text-to-speech uses the built-in macOS `say` command.

---

## Features

- **On-device speech recognition** — `faster-whisper` transcribes microphone
  audio locally (no audio leaves your machine).
- **Natural-language intent parsing** — a lightweight rule-based parser maps
  speech to actions, with English/Hindi keyword support and fuzzy normalization.
- **Desktop actions:**
  - `organize downloads` — moves recent files into a `Downloads/organized` folder
  - `find <name>` — searches Desktop/Documents/Downloads and opens the first match
  - `news` — opens Google News
  - `time` — tells the current time
- **Spoken responses** — replies via macOS text-to-speech.
- **Text mode** — `--text` lets you type commands (no microphone needed) — ideal
  for demos and testing.
- **Clean client/server split** — FastAPI backend is decoupled from the voice
  client, so the same command API can be reused by other front-ends.

---

## Architecture

```
  🎤 mic / ⌨️ text
        │
        ▼
   voice.py  ──HTTP POST /command──▶  server.py (FastAPI)
   (capture +                              │
    speak reply)                           ▼
                                      intent.py  (parse_intent)
                                           │
                                           ▼
                                      actions.py  (handle_action)
                                           │
                                           ▼
                                   organize / find / news / time
```

- `whisper_listen.py` — records and transcribes microphone audio
- `voice.py` — client loop: capture → send → speak (supports `--text`, `--no-voice`)
- `server.py` — FastAPI app exposing `POST /command`
- `intent.py` — rule-based intent parser
- `actions.py` — executes the resolved action
- `utils.py` — logging + response shortening
- `config.py` — centralized paths, limits, and flags

---

## Technologies used

- Python 3.10+
- FastAPI + Uvicorn (command API)
- faster-whisper (local speech-to-text)
- sounddevice + numpy (audio capture)
- macOS `say` (text-to-speech) and `open` (launching files/URLs)

> **Platform note:** TTS (`say`) and file opening (`open`) are macOS-specific.
> The backend, intent parsing, and `--text` mode are cross-platform.

---

## Installation

```bash
git clone <your-repo-url>
cd Jarvis

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env        # optional; sensible defaults are built in
```

---

## Usage

Start the backend in one terminal:

```bash
uvicorn server:app --reload
```

Then start the client in another:

```bash
python voice.py             # microphone mode (macOS)
python voice.py --text      # type commands, no microphone needed
python voice.py --no-voice  # disable spoken replies
```

Say (or type) commands like:

```
organize downloads
find resume
news
time
stop          # exits
```

You can also hit the API directly:

```bash
curl -X POST http://127.0.0.1:8000/command \
     -H "Content-Type: application/json" \
     -d '{"text": "what time is it"}'
```

---

## Screenshots

_Add a terminal screenshot or short screen recording to `screenshots/` and
reference it here._

---

## Testing

Unit tests cover intent parsing, action routing, and the response helpers — all
pure logic, so they need no microphone, server, or audio dependencies:

```bash
pytest -q
```

---

## Future improvements

- AI fallback for unknown commands (the `USE_AI_FALLBACK` flag is already wired
  for this).
- Wake-word detection ("Hey Jarvis") for hands-free activation.
- Cross-platform TTS (e.g. `pyttsx3`) to drop the macOS dependency.
- Continuous listening with voice-activity detection instead of fixed windows.
- More intents (weather, reminders, app launching).

---

## License

Released under the [MIT License](LICENSE).
