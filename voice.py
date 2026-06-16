import argparse
import requests
import subprocess

API_URL = "http://127.0.0.1:8000/command"


def speak(text):
    subprocess.run(["say", text])


def send_command(text):
    try:
        res = requests.post(API_URL, json={"text": text})
        return res.json().get("response", "")
    except Exception as e:
        print("API error:", e)
        return "Server not reachable"


def get_input(text_mode: bool):
    """Return the next command, from the keyboard (text mode) or the mic."""
    if text_mode:
        try:
            return input("You: ").strip().lower()
        except EOFError:
            return "stop"
    # Lazy import so text mode works without audio/whisper dependencies.
    from whisper_listen import listen
    return listen()


def main(text_mode: bool = False, voice_replies: bool = True):
    print("Jarvis system started" + (" (text mode)" if text_mode else ""))
    if voice_replies:
        speak("Jarvis ready")

    while True:
        text = get_input(text_mode)

        if not text:
            continue

        if any(word in text for word in ["exit", "stop", "quit"]):
            if voice_replies:
                speak("Goodbye")
            print("Jarvis: Goodbye")
            break

        print("Sending:", text)

        response = send_command(text)
        print("Jarvis:", response)

        if voice_replies:
            speak(response)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Jarvis voice client")
    parser.add_argument("--text", action="store_true",
                        help="Type commands instead of using the microphone")
    parser.add_argument("--no-voice", action="store_true",
                        help="Disable spoken replies (uses macOS 'say' otherwise)")
    args = parser.parse_args()
    main(text_mode=args.text, voice_replies=not args.no_voice)