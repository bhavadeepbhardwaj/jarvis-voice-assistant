import os
import shutil
import subprocess
import time
from pathlib import Path

DOWNLOADS_PATH = Path.home() / "Downloads"

SEARCH_PATHS = [
    Path.home() / "Desktop",
    Path.home() / "Documents",
    Path.home() / "Downloads"
]

MAX_SEARCH_RESULTS = 5


def organize_downloads(count: int = 20):
    files = sorted(
        DOWNLOADS_PATH.glob("*"),
        key=os.path.getctime,
        reverse=True
    )[:count]

    target_folder = DOWNLOADS_PATH / "organized"
    target_folder.mkdir(exist_ok=True)

    moved = 0

    for file in files:
        if file.is_file():
            shutil.move(str(file), target_folder / file.name)
            moved += 1

    return f"Moved {moved} files"


def find_file(query: str):
    query = query.lower()
    results = []

    for base_path in SEARCH_PATHS:
        for root, _, files in os.walk(base_path):
            for file in files:
                if query in file.lower():
                    full_path = os.path.join(root, file)
                    results.append(full_path)

                    if len(results) >= MAX_SEARCH_RESULTS:
                        break
            if len(results) >= MAX_SEARCH_RESULTS:
                break
        if len(results) >= MAX_SEARCH_RESULTS:
            break

    # --- UX upgrade ---
    if results:
        try:
            subprocess.run(["open", results[0]])  # open first match
        except Exception:
            pass

    return results


def open_news():
    subprocess.run(["open", "https://news.google.com"])
    return "Opened news"


def tell_time():
    return f"The time is {time.strftime('%I:%M %p').lstrip('0')}"


def handle_action(intent: dict):
    action = intent.get("action")
    params = intent.get("params", {})

    if action == "organize_downloads":
        return organize_downloads(**params)

    if action == "find_file":
        return find_file(**params)

    if action == "open_news":
        return open_news()

    if action == "tell_time":
        return tell_time()

    return "I didn’t understand"