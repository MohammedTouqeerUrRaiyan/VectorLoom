import re
import unicodedata


class TextCleaner:
    """
    Cleans extracted document text before chunking.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Cleans extracted text.

        - Normalize unicode
        - Remove tabs
        - Remove extra spaces
        - Remove excessive blank lines
        - Trim whitespace
        """

        if not text:
            return ""

        # Normalize Unicode
        text = unicodedata.normalize("NFKC", text)

        # Replace tabs with spaces
        text = text.replace("\t", " ")

        # Collapse multiple spaces
        text = re.sub(r"[ ]{2,}", " ", text)

        # Collapse multiple blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove leading/trailing whitespace
        text = text.strip()

        return text