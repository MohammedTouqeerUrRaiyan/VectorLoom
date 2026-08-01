from src.preprocessing.validator import DocumentValidator

def test_validator():
    validator = DocumentValidator()

    text = "This is a sample document with enough text for validation."

    valid, msg = validator.validate("data/input/sample1.pdf", text)

    assert isinstance(valid, bool)
    assert isinstance(msg, str)