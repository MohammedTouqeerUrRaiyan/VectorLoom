import os

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".json",
    ".png",
    ".jpg",
    ".jpeg",
    ".bmp",
    ".tiff",
}

class DocumentValidator:

    def validate(self, file_path: str, text: str = ""):

        if not os.path.exists(file_path):
            return False, "File not found"

        extension = os.path.splitext(file_path)[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            return False, "Unsupported file type"

        if text is not None:
            if len(text.strip()) > 0 and len(text.strip()) < 20:
                return False, "Document too short"

        return True, "Valid" 
