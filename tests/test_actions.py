"""Tests for action handling (actions.py). Only side-effect-free paths are
exercised — file-moving/opening actions are not invoked."""

import re

from actions import tell_time, handle_action


def test_tell_time_format():
    out = tell_time()
    assert out.startswith("The time is ")
    # e.g. "The time is 9:05 AM"
    assert re.search(r"\d{1,2}:\d{2}\s?(AM|PM)", out)


def test_handle_action_routes_tell_time():
    result = handle_action({"action": "tell_time", "params": {}})
    assert result.startswith("The time is ")


def test_handle_action_unknown_is_graceful():
    result = handle_action({"action": "definitely_not_a_real_action", "params": {}})
    assert "understand" in result.lower()
