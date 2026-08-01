import pytesseract
from PIL import Image


class OCRProcessor:

    def __init__(self):
        pass

    def extract(self, image_path):

        try:
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text

        except Exception as e:
            print("OCR Error:", e)
            return ""

