from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


class LanguageDetector:

    def detect(self, text: str) -> str:

        if not text:
            return "unknown"

        try:
            return detect(text)
        except Exception:
            return "unknown"