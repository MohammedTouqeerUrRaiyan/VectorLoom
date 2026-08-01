# Changelog

All notable changes to the VectorLoom project are documented in this file.

This project follows a simple versioning approach.

---

# Version 1.0.0

**Release Date:** July 2026

## Added

- Initial project structure.
- PDF document loader.
- DOCX document loader.
- TXT document loader.
- JSON document loader.
- OCR support for image files.
- Metadata extraction module.
- Text cleaning module.
- Text normalization module.
- Language detection module.
- Document validation module.
- Document object implementation.
- Document ingestion pipeline.
- Main application entry point.
- Dataset download script.
- Unit tests using Pytest.
- Project documentation.

---

## Supported File Formats

- PDF (.pdf)
- DOCX (.docx)
- TXT (.txt)
- JSON (.json)
- PNG (.png)
- JPG (.jpg)
- JPEG (.jpeg)
- BMP (.bmp)
- TIFF (.tiff)

---

## Testing

Completed unit tests for:

- PDF Loader
- DOCX Loader
- TXT Loader
- OCR Processor
- Text Cleaner
- Document Validator
- Ingestion Pipeline

### Test Result

```
7 passed
```

---

## Output

Generated:

- Processed text files
- Metadata JSON files

Output directories:

```
data/processed/
data/metadata/
```

---

## Fixed

- Fixed module import issues.
- Fixed package structure for `src`.
- Fixed PDF loader path errors.
- Fixed DOCX loader path errors.
- Fixed TXT loader path errors.
- Fixed validator function parameters.
- Fixed unit test import issues.
- Fixed project execution using:

```bash
python -m src.main
```

---

## Documentation

Created the following documentation:

- README.md
- Installation.md
- Architecture.md
- Developer_Guide.md
- User_Guide.md
- API.md
- CHANGELOG.md

---

# Future Improvements

Planned enhancements include:

- Vector Embeddings
- FAISS Integration
- ChromaDB Integration
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- REST API
- Large Language Model (LLM) Integration

---

# Version History

| Version | Status | Description |
|---------|--------|-------------|
| 1.0.0 | Released | Initial release of the VectorLoom document ingestion pipeline. |