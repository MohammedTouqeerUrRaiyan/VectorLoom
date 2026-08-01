from src.ingestion.pdf_loader import PDFLoader

def test_pdf_loader():
    loader = PDFLoader()

    pages = loader.load("data/input/sample1.pdf")

    assert isinstance(pages, list)
    assert len(pages) > 0

    for page in pages:
        assert isinstance(page, str) 

        