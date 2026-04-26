import struct

class ProtocolParser:
    def __init__(self):
        self.HEADER_SIZE = 4

    def parse_hex(self, hex_str: str) -> dict:
        # Clean input and convert to bytes
        binary_data = bytes.fromhex(hex_str.replace(" ", ""))

        if len(binary_data) < self.HEADER_SIZE:
            raise ValueError("Frame too short for header")
        
        # Unpack first 4 bytes (B = unsigned char, 1 byte)
        b0, b1, class_id, msg_id = struct.unpack('<BBBB', binary_data[:4])

        #BGAPI-style length and type extraction
        msg_type = "Event" if (b0 & 0x80) else "Command"
        payload_len = ((b0 & 0x7F) << 8) | b1

        payload = binary_data[4:4 + payload_len]

        return {
            "type": msg_type,
            "length": payload_len,
            "class": hex(class_id),
            "id": hex(msg_id),
            "payload": payload.hex().upper()
        }