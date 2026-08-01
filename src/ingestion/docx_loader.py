from docx import Document

class DocxLoader:
    def load(self, file_path: str) -> str:
        """
        Load the content of a DOCX file.

        Args:
            file_path (str): The path to the DOCX file.

        Returns:
            str: The text content of the DOCX file.
        """
        document = Document(file_path)
        full_text = []
        for paragraph in document.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)