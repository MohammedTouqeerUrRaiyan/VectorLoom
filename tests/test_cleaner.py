from src.preprocessing.cleaner import TextCleaner

def test_cleaner():
    cleaner = TextCleaner()
    result = cleaner.clean("Hello   World!")
    assert result is not None