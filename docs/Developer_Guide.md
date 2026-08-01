# Developer Guide

## Introduction

This guide is intended for developers who want to understand, maintain, or extend the VectorLoom document ingestion pipeline. It explains the project structure, module responsibilities, development workflow, and coding guidelines.

---

# Project Overview

VectorLoom is a modular document ingestion system that:

- Loads documents from multiple formats.
- Extracts text and metadata.
- Cleans and normalizes text.
- Detects document language.
- Validates document content.
- Stores processed text and metadata.
- Provides a pipeline suitable for AI and RAG applications.

---

# Project Structure

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
│
├── notebooks/
│
├── models/
│
├── src/
│   ├── ingestion/
│   │   ├── pdf_loader.py
│   │   ├── docx_loader.py
│   │   ├── txt_loader.py
│   │   ├── json_loader.py
│   │   ├── ocr.py
│   │   ├── metadata_extractor.py
│   │   ├── document.py
│   │   └── pipeline.py
│   │
│   ├── preprocessing/
│   │   ├── cleaner.py
│   │   ├── normalizer.py
│   │   ├── language_detector.py
│   │   └── validator.py
│   │
│   └── main.py
│
├── tests/
│
└── requirements.txt
```

---

# Module Responsibilities

## Ingestion Module

Responsible for reading different document formats.

Components:

- PDFLoader
- DocxLoader
- TxtLoader
- JsonLoader
- OCRProcessor
- MetadataExtractor
- Document
- IngestionPipeline

---

## Preprocessing Module

Responsible for preparing extracted text.

Components:

- TextCleaner
- TextNormalizer
- LanguageDetector
- DocumentValidator

---

# Pipeline Workflow

```
Input Document
      │
      ▼
Document Loader
      │
      ▼
Extract Text
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
Validation
      │
      ▼
Document Object
      │
      ▼
Save Output
```

---

# Running the Project

Navigate to the project directory:

```bash
cd D:\vectorloom
```

Run the application:

```bash
python -m src.main
```

Run all tests:

```bash
python -m pytest
```

---

# Coding Guidelines

- Follow PEP 8 style guidelines.
- Use meaningful class and variable names.
- Keep modules focused on a single responsibility.
- Add comments where complex logic is implemented.
- Write unit tests for new functionality.

---

# Testing

The project includes tests for:

- PDF Loader
- DOCX Loader
- TXT Loader
- OCR
- Cleaner
- Validator
- Pipeline

Run tests:

```bash
python -m pytest
```

Expected output:

```
7 passed
```

---

# Adding a New Loader

To support another file type:

1. Create a new loader in `src/ingestion/`.
2. Implement a `load()` method.
3. Update `pipeline.py` to route the new file extension.
4. Add a unit test in the `tests/` directory.
5. Verify all tests pass.

---

# Output

Processed text:

```
data/processed/
```

Metadata:

```
data/metadata/
```

---

# Future Development

Possible enhancements include:

- Embedding generation
- Vector database integration (FAISS, ChromaDB)
- Semantic search
- Retrieval-Augmented Generation (RAG)
- LLM integration
- REST API for document ingestion

---

# Contributors

Developed as part of the **VectorLoom AI Document Ingestion Pipeline** project.