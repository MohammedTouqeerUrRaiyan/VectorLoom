from pathlib import Path
import fitz  # PyMuPDF


class PDFLoader:
    """
    Extracts text from PDF documents using PyMuPDF.
    """

    @staticmethod
    def load(file_path: Path) -> tuple[str, int]:
        """
        Reads a PDF file and returns:
            - extracted text
            - total number of pages
        """

        document = fitz.open(file_path)

        pages = len(document)

        extracted_text = []

        for page in document:

            extracted_text.append(page.get_text("text"))

        document.close()

        full_text = "\n".join(extracted_text)

        return full_text, pages