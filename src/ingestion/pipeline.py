import os

from .pdf_loader import PDFLoader
from .docx_loader import DocxLoader
from .txt_loader import TxtLoader
from .ocr import OCRProcessor
from .metadata_extractor import MetadataExtractor
from .document import Document
from .json_loader import JsonLoader

from src.preprocessing.cleaner import TextCleaner
from src.preprocessing.normalizer import TextNormalizer
from src.preprocessing.language_detector import LanguageDetector
from src.preprocessing.validator import DocumentValidator


class IngestionPipeline:

    def __init__(self):
        self.pdf_loader = PDFLoader()
        self.docx_loader = DocxLoader()
        self.txt_loader = TxtLoader()
        self.ocr = OCRProcessor()
        self.json_loader = JsonLoader()

        self.metadata_extractor = MetadataExtractor()

        self.cleaner = TextCleaner()
        self.normalizer = TextNormalizer()
        self.language_detector = LanguageDetector()
        self.validator = DocumentValidator()

    def run(self, file_path):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            text = self.pdf_loader.load(file_path)

        elif extension == ".docx":
            text = self.docx_loader.load(file_path)

        elif extension == ".txt":
            text = self.txt_loader.load(file_path)

        elif extension in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
            text = self.ocr.extract(file_path)

        elif extension == ".json":
            text = self.json_loader.load(file_path)

        else:
            return Document(
                source_path=file_path,
                extracted_text="",
                clean_text="",
                metadata={},
                language="unknown",
                valid=False,
                error="Unsupported file type",
            )

        valid, error = self.validator.validate(file_path, text)

        if not valid:
            return Document(
                source_path=file_path,
                extracted_text=text,
                clean_text="",
                metadata={},
                language="unknown",
                valid=False,
                error=error,
            )

        clean_text = self.cleaner.clean(text)
        normalized_text = self.normalizer.normalize(clean_text)
        language = self.language_detector.detect(normalized_text)

        metadata = self.metadata_extractor.extract(file_path)
        metadata["language"] = language

        return Document(
            source_path=file_path,
            extracted_text=text,
            clean_text=normalized_text,
            metadata=metadata,
            language=language,
            valid=True,
            error=None,
        )
    