import re


class TextNormalizer:

    def normalize(self, text):
        if not text:
            return ""

        # Convert to lowercase
        text = text.lower()

        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)

        return text.strip()
