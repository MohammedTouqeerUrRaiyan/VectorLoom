from pathlib import Path

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
    """
    Complete document ingestion pipeline.

    Flow:
        File
        ↓
        Loader / OCR
        ↓
        Validation
        ↓
        Cleaning
        ↓
        Normalization
        ↓
        Language Detection
        ↓
        Metadata Extraction
        ↓
        Standardized Document
    """

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

        file_path = Path(file_path)

        extension = file_path.suffix.lower()

        # --------------------------------------------------
        # 1. LOAD DOCUMENT
        # --------------------------------------------------

        if extension == ".pdf":

            text, pages = self.pdf_loader.load(file_path)

        elif extension == ".docx":

            text, pages = self.docx_loader.load(file_path)

        elif extension == ".txt":

            text, pages = self.txt_loader.load(file_path)

        elif extension in [
            ".png",
            ".jpg",
            ".jpeg",
            ".bmp",
            ".tiff",
        ]:

            text = self.ocr.extract(file_path)

            # Images are treated as one logical page.
            pages = 1

        elif extension == ".json":

            text = self.json_loader.load(file_path)

            # JSON has no physical pages.
            pages = 1

        else:

            return Document(
                source_path=str(file_path),
                extracted_text="",
                clean_text="",
                pages=0,
                metadata={},
                language="unknown",
                valid=False,
                error=f"Unsupported file type: {extension}",
            )

        # --------------------------------------------------
        # 2. VALIDATE DOCUMENT
        # --------------------------------------------------

        valid, error = self.validator.validate(
            file_path,
            text,
        )

        if not valid:

            return Document(
                source_path=str(file_path),
                extracted_text=text,
                clean_text="",
                pages=pages,
                metadata={},
                language="unknown",
                valid=False,
                error=error,
            )

        # --------------------------------------------------
        # 3. CLEAN TEXT
        # --------------------------------------------------

        clean_text = self.cleaner.clean(text)

        # --------------------------------------------------
        # 4. NORMALIZE TEXT
        # --------------------------------------------------

        normalized_text = self.normalizer.normalize(
            clean_text
        )

        # --------------------------------------------------
        # 5. DETECT LANGUAGE
        # --------------------------------------------------

        language = self.language_detector.detect(
            normalized_text
        )

        # --------------------------------------------------
        # 6. EXTRACT METADATA
        # --------------------------------------------------

        metadata = self.metadata_extractor.extract(
            file_path
        )

        metadata["language"] = language
        metadata["pages"] = pages

        # --------------------------------------------------
        # 7. CREATE STANDARD DOCUMENT
        # --------------------------------------------------

        return Document(
            source_path=str(file_path),
            extracted_text=text,
            clean_text=normalized_text,
            pages=pages,
            metadata=metadata,
            language=language,
            valid=True,
            error=None,
        )