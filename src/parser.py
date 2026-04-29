import struct
import logging
from src.utils import Checksum
from src.protocol import MsgClass

logger = logging.getLogger(__name__)

class ProtocolParser:
    def __init__(self):
        self.HEADER_SIZE = 4
        self.CRC_SIZE = 2

    def parse_hex(self, hex_str: str) -> dict:
        logger.debug(f"Parsing input: {hex_str}")

        try:
            # Clean input and convert to bytes
            binary_data = bytes.fromhex(hex_str.replace(" ", ""))
        except ValueError as e:
            logger.error(f"Invalid hexadecimal input: {hex_str}")
            raise ValueError(f"Invalid hex string: {e}")

        if len(binary_data) < (self.HEADER_SIZE + self.CRC_SIZE):
            logger.warning(f"Input too short: {len(binary_data)} bytes")
            raise ValueError("Frame too short")
        
        # Unpack first 4 bytes (B = unsigned char, 1 byte)
        b0, b1, class_id, msg_id = struct.unpack('<BBBB', binary_data[:4])
        payload_len = ((b0 & 0x7F) << 8) | b1

        total_expected_size = self.HEADER_SIZE + payload_len + self.CRC_SIZE
        if len(binary_data) < total_expected_size:
            logger.error(f"Incomplete frame. Expected {total_expected_size}, got {len(binary_data)}")
            raise ValueError(f"Incomplete frame. Expected {total_expected_size} bytes.")

        # CRC Verification
        # CRC is calculated over the Header + Payload
        data_to_check = binary_data[:self.HEADER_SIZE + payload_len]
        received_crc = struct.unpack('<H', binary_data[total_expected_size-2:total_expected_size])[0]
        calculated_crc = Checksum.crc16(data_to_check)

        if received_crc != calculated_crc:
            logger.error(f"CRC Error! Received: {hex(received_crc)}, Calculated: {hex(calculated_crc)}")
            raise ValueError(f"CRC Mismatch: Received {hex(received_crc)}, Calculated {hex(calculated_crc)}")

        class_name = "UNKNOWN"
        for item in MsgClass:
            if item.value == class_id:
                class_name = item.name
                break
        
        logger.info(f"Successfully parsed {class_name} {msg_id}")

        return {
            "type": "Event" if (b0 & 0x80) else "Command",
            "length": payload_len,
            "class": class_name,
            "id": hex(msg_id),
            "payload": binary_data[4:4 + payload_len].hex().upper()
        }