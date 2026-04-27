import struct
from src.utils import Checksum

class ProtocolParser:
    def __init__(self):
        self.HEADER_SIZE = 4
        self.CRC_SIZE = 2

    def parse_hex(self, hex_str: str) -> dict:
        # Clean input and convert to bytes
        binary_data = bytes.fromhex(hex_str.replace(" ", ""))

        if len(binary_data) < (self.HEADER_SIZE + self.CRC_SIZE):
            raise ValueError("Frame too short")
        
        # Unpack first 4 bytes (B = unsigned char, 1 byte)
        b0, b1, class_id, msg_id = struct.unpack('<BBBB', binary_data[:4])
        payload_len = ((b0 & 0x7F) << 8) | b1

        total_expected_size = self.HEADER_SIZE + payload_len + self.CRC_SIZE
        if len(binary_data) < total_expected_size:
            raise ValueError(f"Incomplete frame. Expected {total_expected_size} bytes.")

        # CRC Verification
        # CRC is calculated over the Header + Payload
        data_to_check = binary_data[:self.HEADER_SIZE + payload_len]
        received_crc = struct.unpack('<H', binary_data[total_expected_size-2:total_expected_size])[0]
        calculated_crc = Checksum.crc16(data_to_check)

        if received_crc != calculated_crc:
            raise ValueError(f"CRC Mismatch: Received {hex(received_crc)}, Calculated {hex(calculated_crc)}")

        return {
            "type": "Event" if (b0 & 0x80) else "Command",
            "length": payload_len,
            "class": hex(class_id),
            "id": hex(msg_id),
            "payload": binary_data[4:4 + payload_len].hex().upper()
        }