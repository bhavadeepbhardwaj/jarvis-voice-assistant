import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

model = WhisperModel("base", compute_type="int8")

SAMPLE_RATE = 16000


def listen():
    print("🎤 Listening...")

    duration = 2.0  # keep it short for speed

    audio = sd.rec(int(duration * SAMPLE_RATE),
                   samplerate=SAMPLE_RATE,
                   channels=1,
                   dtype="float32")

    sd.wait()

    audio = np.squeeze(audio)

    segments, _ = model.transcribe(
        audio,
        language="en",
        beam_size=1,
        vad_filter=True
    )

    text = " ".join([seg.text for seg in segments]).strip().lower()

    if text:
        print("You said:", text)
        return text

    return None