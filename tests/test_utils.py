"""Tests for response helpers (utils.py)."""

from utils import short_response


def test_short_response_lists_filenames():
    result = ["/Users/me/Desktop/report.pdf", "/tmp/notes.txt"]
    out = short_response(result, "find report")
    assert out == "report.pdf, notes.txt"


def test_short_response_empty_list():
    assert short_response([], "find nothing") == "No files found"


def test_short_response_truncates_long_string():
    long = "x" * 200
    assert len(short_response(long, "cmd")) == 60


def test_short_response_other_type():
    assert short_response({"k": "v"}, "cmd") == "Done"
