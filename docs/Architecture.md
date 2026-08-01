# System Architecture

## Overview

VectorLoom is an AI-powered document ingestion pipeline that processes multiple document formats and prepares them for Retrieval-Augmented Generation (RAG) systems. The pipeline extracts text, preprocesses it, validates documents, and stores processed output with metadata.

---

# Architecture Diagram

```
                +----------------------+
                |   Input Documents    |
                |----------------------|
                | PDF                  |
                | DOCX                 |
                | TXT                  |
                | JSON                 |
                | Images (OCR)         |
                +----------+-----------+
                           |
                           ▼
                 +--------------------+
                 | Document Loaders   |
                 |--------------------|
                 | PDF Loader         |
                 | DOCX Loader        |
                 | TXT Loader         |
                 | JSON Loader        |
                 | OCR Processor      |
                 +----------+---------+
                            |
                            ▼
               +-------------------------+
               | Metadata Extraction     |
               +-----------+-------------+
                           |
                           ▼
               +-------------------------+
               | Text Cleaning           |
               +-----------+-------------+
                           |
                           ▼
               +-------------------------+
               | Text Normalization      |
               +-----------+-------------+
                           |
                           ▼
               +-------------------------+
               | Language Detection      |
               +-----------+-------------+
                           |
                           ▼
               +-------------------------+
               | Document Validation     |
               +-----------+-------------+
                           |
                           ▼
               +-------------------------+
               | Document Object         |
               +-----------+-------------+
                           |
                           ▼
             +----------------------------+
             | Output                     |
             |----------------------------|
             | Processed Text (.txt)      |
             | Metadata (.json)           |
             +----------------------------+
```

---

# Components

## 1. Document Loaders

The ingestion module supports:

- PDF Loader
- DOCX Loader
- TXT Loader
- JSON Loader
- OCR Processor

These components extract text from different file formats.

---

## 2. Metadata Extractor

Extracts metadata such as:

- File name
- File size
- File type
- Creation time
- Modification time
- Language

---

## 3. Preprocessing

The preprocessing module performs:

- Text Cleaning
- Text Normalization
- Language Detection
- Document Validation

---

## 4. Document Object

The processed information is stored in a Document object containing:

- Source Path
- Extracted Text
- Clean Text
- Metadata
- Language
- Validation Status
- Error Message

---

## 5. Output

The pipeline stores:

Processed Text

```
data/processed/
```

Metadata

```
data/metadata/
```

---

# Project Workflow

```
Input File
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
Save Processed Text
     │
     ▼
Save Metadata
```

---

# Technologies Used

- Python
- PyMuPDF
- python-docx
- pytesseract
- Pillow
- langdetect
- pytest

---

# Advantages

- Modular architecture
- Supports multiple document formats
- Easy to extend
- Unit tested
- Suitable for AI and RAG pipelines
- Clean separation between ingestion and preprocessing modules

---

# Future Enhancements

- Vector Embeddings
- FAISS Integration
- ChromaDB Integration
- Semantic Search
- Retrieval-Augmented Generation (RAG)
- Large Language Model (LLM) Integration 