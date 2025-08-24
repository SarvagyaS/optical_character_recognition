"""Run recognizer as a module: python -m passport_ocr <image_path>"""
import sys
from .recognition import recognize_passport

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python -m passport_ocr <image_path>')
        sys.exit(1)
    image_path = sys.argv[1]
    out = recognize_passport(image_path)
    import json
    print(json.dumps(out, indent=2))
