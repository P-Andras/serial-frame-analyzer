import pytest
from src.parser import ProtocolParser

def test_valid_command_parsing():
    parser = ProtocolParser()
    # Header: 00 02 01 05 | Payload: AA BB | CRC: D2 33
    raw = "00020105AABBD233"
    result = parser.parse_hex(raw)
    
    assert result["type"] == "Command"
    assert result["length"] == 2
    assert result["class"] == "0x1"
    assert result["id"] == "0x5"
    assert result["payload"] == "AABB"

def test_valid_event_parsing():
    parser = ProtocolParser()
    # Header: 80 01 02 03 | Payload: FF | CRC: AB 60
    raw = "80010203FFAB60"
    result = parser.parse_hex(raw)
    
    assert result["type"] == "Event"
    assert result["length"] == 1
    assert result["class"] == "0x2"
    assert result["id"] == "0x3"
    assert result["payload"] == "FF"

def test_short_frame_raises_error():
    parser = ProtocolParser()
    raw = "000101"
    
    # Updated match to match the code's current error string
    with pytest.raises(ValueError, match="Frame too short"):
        parser.parse_hex(raw)

def test_invalid_hex_raises_error():
    parser = ProtocolParser()
    raw = "ZZZZZZ"
    
    with pytest.raises(ValueError):
        parser.parse_hex(raw)

def test_corrupted_crc_raises_error():
    parser = ProtocolParser()
    # Valid: 00 01 01 01 | Payload: FF | CRC: 49 7D
    valid_frame = "00010101FF497D" 
    corrupted_frame = "00010101FF0000" 
    
    # This should pass
    assert parser.parse_hex(valid_frame)["payload"] == "FF"
    
    # This must fail
    with pytest.raises(ValueError, match="CRC Mismatch"):
        parser.parse_hex(corrupted_frame)