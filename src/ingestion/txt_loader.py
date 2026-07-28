from pathlib import Path


class TextLoader:
    """
    Loads plain text (.txt) documents.
    """

    @staticmethod
    def load(file_path: Path) -> tuple[str, int]:
        """
        Reads a text file and returns:
            - extracted text
            - page count (always 1 for text files)
        """

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            text = file.read()

        return text, 1