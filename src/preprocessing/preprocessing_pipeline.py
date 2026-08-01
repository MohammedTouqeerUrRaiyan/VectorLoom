from .cleaner import TextCleaner
from .normalizer import TextNormalizer
from .language_detector import LanguageDetector
from .validator import DocumentValidator


class PreprocessingPipeline:

    def __init__(self):

        self.cleaner = TextCleaner()
        self.normalizer = TextNormalizer()
        self.language_detector = LanguageDetector()
        self.validator = DocumentValidator()

    def process(self, file_path: str, text: str):

        valid, error = self.validator.validate(file_path, text)

        if not valid:
            return False, error

        clean_text = self.cleaner.clean(text)
        normalized_text = self.normalizer.normalize(clean_text)
        language = self.language_detector.detect(normalized_text)

        return True, {
            "clean_text": clean_text,
            "normalized_text": normalized_text,
            "language": language,
        }