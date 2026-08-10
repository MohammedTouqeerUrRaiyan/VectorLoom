import chardet

from src.logging.logger import setup_logger

logger = setup_logger(__name__)


class TxtLoader:
    """
    Text file loader with automatic encoding detection.

    Supports UTF-8, UTF-16, Windows encodings,
    and other encodings detected by chardet.
    """

    @staticmethod
    def load(file_path: str) -> tuple[str, int]:
        """
        Load text from a TXT file.

        Returns:
            tuple[str, int]: Extracted text and logical page count.
        """

        logger.info("Loading TXT file: %s", file_path)

        with open(file_path, "rb") as f:
            raw_data = f.read(10000)

        result = chardet.detect(raw_data)

        encoding = result.get("encoding")
        confidence = result.get("confidence", 0)

        if not encoding:
            logger.warning(
                "Could not detect encoding for %s. Falling back to UTF-8.",
                file_path,
            )
            encoding = "utf-8"

        logger.debug(
            "Detected encoding=%s confidence=%.2f",
            encoding,
            confidence,
        )

        try:
            with open(
                file_path,
                "r",
                encoding=encoding,
                errors="replace",
            ) as f:
                text = f.read()

        except (UnicodeDecodeError, LookupError):
            logger.warning(
                "Failed to read %s using encoding=%s. "
                "Falling back to UTF-8.",
                file_path,
                encoding,
            )

            with open(
                file_path,
                "r",
                encoding="utf-8",
                errors="replace",
            ) as f:
                text = f.read()

        logger.info(
            "TXT file loaded successfully. Characters=%d",
            len(text),
        )

        return text, 1