import fitz # pyMuPDF
from typing import List

class PDFLoader:
    def load(self, file_path: str) -> List[str]:
        pages = []
        with fitz.open(file_path) as doc:
            for page in doc:
                pages.append(page.get_text())
        return pages
      