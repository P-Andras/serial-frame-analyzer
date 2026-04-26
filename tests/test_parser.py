import pytest
from src.parser import ProtocolParser

def test_valid_command_parsing():
    parser = ProtocolParser()
    raw = "00020105AABB"
    result = parser.parse_hex(raw)

    assert result["type"] == "Command"
    assert result["length"] == 2
    assert result["class"] == "0x1"
    assert result["id"] == "0x5"
    assert result["payload"] == "AABB"

def test_valid_event_parsing():
    parser = ProtocolParser()
    raw = "80010203FF"
    result = parser.parse_hex(raw)

    assert result["type"] == "Event"
    assert result["length"] == 1
    assert result["class"] == "0x2"
    assert result["id"] == "0x3"
    assert result["payload"] == "FF"

def test_short_frame_raises_error():
    parser = ProtocolParser()
    raw = "000101"

    with pytest.raises(ValueError, match="Frame too short for header"):
        parser.parse_hex(raw)


def test_invalid_hex_raises_error():
    parser = ProtocolParser()
    raw = "ZZZZZZ"

    with pytest.raises(ValueError):
        parser.parse_hex(raw)

