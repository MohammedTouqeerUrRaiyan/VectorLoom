from src.ingestion.docx_loader import DocxLoader

def test_docx_loader():
    loader = DocxLoader()
    text = loader.load("data/input/sample2.docx")
    assert text is not None