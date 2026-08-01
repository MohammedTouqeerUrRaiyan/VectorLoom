# VectorLoom

## Overview

VectorLoom is an AI-powered document ingestion pipeline designed to process multiple document formats for Retrieval-Augmented Generation (RAG) applications. The system extracts text, cleans and normalizes it, detects language, validates documents, and stores processed output with metadata.

---

## Features

- PDF Loader
- DOCX Loader
- TXT Loader
- JSON Loader
- OCR Integration
- Metadata Extraction
- Text Cleaning
- Text Normalization
- Language Detection
- Document Validation
- Document Processing Pipeline
- Unit Testing with Pytest

---

## Project Structure

```
vectorloom/
│
├── data/
│   ├── input/
│   ├── raw/
│   ├── processed/
│   └── metadata/
│
├── docs/
│   ├── API.md
│   ├── Architecture.md
│   ├── CHANGELOG.md
│   ├── Developer_Guide.md
│   ├── Installation.md
│   ├── README.md
│   └── User_Guide.md
│
├── models/
│
├── notebooks/
│
├── src/
│   ├── ingestion/
│   ├── preprocessing/
│   └── main.py
│
├── tests/
│
├── download_dataset.py
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.10+
- PyMuPDF
- python-docx
- pytesseract
- Pillow
- langdetect
- pytest

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Dataset

The project uses the EnterpriseRAG sample dataset.

Raw dataset location:

```
data/raw/enterprise_rag/
```

Example files:

```
documents_sample.json
questions_sample.json
```

---

## Running the Project

Download the dataset:

```bash
python download_dataset.py
```

Run the application:

```bash
python -m src.main
```

---

## Running Tests

Run all tests:

```bash
python -m pytest
```

Expected result:

```
7 passed
```

---

## Processing Workflow

```
Input Document
      │
      ▼
Document Loader
      │
      ▼
OCR (Images)
      │
      ▼
Metadata Extraction
      │
      ▼
Text Cleaning
      │
      ▼
Normalization
      │
      ▼
Language Detection
      │
      ▼
Document Validation
      │
      ▼
Processed Text
      │
      ▼
Metadata Output
```

---

## Supported File Types

| Format | Supported |
|---------|-----------|
| PDF | Yes |
| DOCX | Yes |
| TXT | Yes |
| JSON | Yes |
| PNG | Yes |
| JPG | Yes |
| JPEG | Yes |
| BMP | Yes |
| TIFF | Yes |

---

## Output

Processed text:

```
data/processed/
```

Metadata:

```
data/metadata/
```

---

## Testing

The project contains unit tests for:

- PDF Loader
- DOCX Loader
- TXT Loader
- OCR
- Validator
- Cleaner
- Pipeline

---

## Technologies Used

- Python
- PyMuPDF
- python-docx
- pytesseract
- Pillow
- langdetect
- pytest

---

## Future Enhancements

- Embedding Generation
- FAISS Vector Database
- ChromaDB Integration
- OpenAI Embeddings
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- LLM Integration

---

## Author

Developed as part of the VectorLoom AI Document Ingestion Pipeline project.