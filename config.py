import os
from pathlib import Path

# --- Server ---
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 8000))

# --- Base Paths ---
HOME = Path.home()
DOWNLOADS_PATH = HOME / "Downloads"
DESKTOP_PATH = HOME / "Desktop"
DOCUMENTS_PATH = HOME / "Documents"

# Centralized search scope (used in actions.py)
SEARCH_PATHS = [
    DESKTOP_PATH,
    DOCUMENTS_PATH,
    DOWNLOADS_PATH
]

# --- Limits ---
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", 5))
MAX_ORGANIZE_FILES = int(os.getenv("MAX_ORGANIZE_FILES", 50))

# --- Performance ---
SEARCH_TIMEOUT_SEC = 2          # prevent long blocking scans
MAX_SCAN_DEPTH = 5             # limit recursion depth

# --- OpenAI (for later use only; see USE_AI_FALLBACK) ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")   # fast + cheap fallback model

# --- Behavior Flags ---
USE_AI_FALLBACK = os.getenv("USE_AI_FALLBACK", "false").lower() == "true"
DEBUG = os.getenv("DEBUG", "true").lower() == "true"

# --- Response ---
MAX_RESPONSE_CHARS = 60