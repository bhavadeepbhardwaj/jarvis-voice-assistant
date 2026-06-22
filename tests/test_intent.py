"""Tests for the rule-based intent parser (intent.py). Pure logic, no I/O."""

from intent import (
    parse_intent,
    normalize,
    extract_number,
    extract_query,
    detect_language,
)


def test_organize_downloads_intent():
    i = parse_intent("organize downloads")
    assert i["action"] == "organize_downloads"
    assert i["params"]["count"] == 20  # default


def test_find_file_intent_extracts_query():
    i = parse_intent("find resume")
    assert i["action"] == "find_file"
    assert i["params"]["query"] == "resume"


def test_news_intent_beats_single_word_fallback():
    assert parse_intent("news")["action"] == "open_news"


def test_time_intent():
    assert parse_intent("time")["action"] == "tell_time"
    assert parse_intent("what time is it")["action"] == "tell_time"


def test_single_word_falls_back_to_find():
    i = parse_intent("budget")
    assert i["action"] == "find_file"
    assert i["params"]["query"] == "budget"


def test_unknown_intent():
    assert parse_intent("hello there friend")["action"] == "unknown"


def test_normalize_fixes_common_typos():
    assert normalize("  ORGANISE my Downlods ") == "organize my downloads"
    assert normalize("resum") == "resume"


def test_extract_number_default_and_match():
    assert extract_number("organize 7 files") == 7
    assert extract_number("organize files") == 20


def test_extract_query_with_for():
    assert extract_query("find for my report") == "my report"


def test_detect_language_hindi():
    assert detect_language("समय") == "hi"
    assert detect_language("time") == "en"
