## Component Design: ProtocolParser

The parser will use a "Functional Transformation" approach:
1. **Input:** Hexadecimal string (e.g., "00010101FF").
2. **Validation:** Check if length >= 4 bytes.
3. **Extraction:** - `Type`: Bit 7 of Byte 0.
   - `Length`: Bits 0-6 of Byte 0 + Byte 1.
   - `Class/ID`: Bytes 2 and 3.
4. **Output:** A Python dictionary for easy JSON serialization.