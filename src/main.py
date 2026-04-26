import sys
from src.parser import ProtocolParser

def run():
    if len(sys.argv) < 2:
        print("Usage: python3 -m src.main <HEX_STRING>")
        return
    
    hex_input = sys.argv[1]
    parser = ProtocolParser()

    try:
        result = parser.parse_hex(hex_input)
        print("--- Decoded Frame ---")
        for key, value in result.items():
            print(f"{key.capitalize()}: {value}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    run()