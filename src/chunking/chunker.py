import re
import unicodedata


class TextCleaner:
    """
    Cleans raw extracted document text before chunking.
    """

    @staticmethod
    def clean(text: str) -> str:
        """
        Perform basic preprocessing on extracted text.

        Args:
            text: Raw extracted document text.

        Returns:
            Cleaned text.
        """

        if not text:
            return ""

        # Normalize unicode
        text = unicodedata.normalize("NFKC", text)

        # Replace tabs with spaces
        text = text.replace("\t", " ")

        # Remove multiple spaces
        text = re.sub(r"[ ]+", " ", text)

        # Remove excessive blank lines
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Strip whitespace
        text = text.strip()

        return text