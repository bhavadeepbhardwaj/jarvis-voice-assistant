from typing import Dict
import re


def detect_language(text: str) -> str:
    hindi_chars = any('\u0900' <= c <= '\u097F' for c in text)
    return "hi" if hindi_chars else "en"


def extract_number(text: str, default: int = 20) -> int:
    match = re.search(r"\d+", text)
    return int(match.group()) if match else default


def extract_query(text: str) -> str:
    match = re.search(r"(find|search|look)( for)?\s+(.*)", text.lower())
    return match.group(3).strip() if match else text.strip()


def normalize(text: str) -> str:
    text = text.lower().strip()

    # Whole-word replacements only. Substring replacement caused cascades
    # (e.g. "resume" -> "resumee", "downloads" -> "downloadss").
    replacements = {
        "resum": "resume",
        "downlods": "downloads",
        "download": "downloads",
        "organised": "organize",
        "organise": "organize",
    }

    words = [replacements.get(w, w) for w in text.split()]
    return " ".join(words)


def parse_intent(text: str) -> Dict:
    text_lower = normalize(text)
    lang = detect_language(text_lower)

    words = text_lower.split()

    # --- ORGANIZE DOWNLOADS ---
    if any(word in text_lower for word in [
        "organize", "organise", "organised", "sort", "clean"
    ]):
        if "download" in text_lower or "downloads" in text_lower or len(words) == 1:
            return {
                "action": "organize_downloads",
                "params": {"count": extract_number(text_lower)},
                "lang": lang
            }

    # --- FIND FILE ---
    if any(word in text_lower for word in [
        "find", "search", "look", "dhund", "dhundo"
    ]):
        query = extract_query(text_lower)

        # fallback if extraction fails
        if query in ["find", "search", "look", ""]:
            query = text_lower

        return {
            "action": "find_file",
            "params": {"query": query},
            "lang": lang
        }

    # --- NEWS ---
    if any(word in text_lower for word in [
        "news", "khabar", "headlines"
    ]):
        return {
            "action": "open_news",
            "params": {},
            "lang": lang
        }

    # --- TIME ---
    if any(word in text_lower for word in [
        "time", "clock", "samay"
    ]):
        return {
            "action": "tell_time",
            "params": {},
            "lang": lang
        }

    # single-word fallback (VERY important for voice): treat a lone word as a
    # file search, but only after the known command keywords above.
    if len(words) == 1:
        return {
            "action": "find_file",
            "params": {"query": text_lower},
            "lang": lang
        }

    return {
        "action": "unknown",
        "params": {"raw": text},
        "lang": lang
    }
