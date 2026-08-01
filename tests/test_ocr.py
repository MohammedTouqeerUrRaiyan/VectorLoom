from src.ingestion.ocr import OCRProcessor

def test_ocr():
    ocr = OCRProcessor()
    assert ocr is not None