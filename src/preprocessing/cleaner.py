import re

class TextCleaner:
    def clean(self, text: str) -> str:
        if not text:
            return ""

        # Remove URLs
        text = re.sub(r"http\S+|www\S+", "", text)

        # Remove HTML tags
        text = re.sub(r"<.*?>", "", text)

        # Remove extra spaces
        text = re.sub(r"\s+", " ", text)

        # Remove unwanted characters
        text = re.sub(r"[^\w\s.,!?@()\-\:/]", "", text)

        return text.strip()
