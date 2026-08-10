from src.ingestion.txt_loader import TxtLoader

def test_txt_loader():
    loader = TxtLoader()

    text = loader.load("data/input/sample3.txt")

    assert isinstance(text, list)
    assert len(text) > 0
