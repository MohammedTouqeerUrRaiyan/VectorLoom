# API Documentation

## Overview

This document describes the main classes, methods, inputs, outputs, and responsibilities of the VectorLoom document ingestion pipeline.

---

# Package Structure

```
src/
├── ingestion/
├── preprocessing/
└── main.py
```

---

# Ingestion Module

## PDFLoader

### Description

Loads PDF documents and extracts text from all pages.

### Method

```python
load(file_path: str) -> str
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| file_path | str | Path to the PDF file |

### Returns

```
Extracted text from the PDF.
```

---

## DocxLoader

### Description

Loads Microsoft Word documents.

### Method

```python
load(file_path: str) -> str
```

### Parameters

| Parameter | Type |
|-----------|------|
| file_path | str |

### Returns

```
Extracted document text.
```

---

## TxtLoader

### Description

Loads plain text files.

### Method

```python
load(file_path: str) -> str
```

### Parameters

| Parameter | Type |
|-----------|------|
| file_path | str |

### Returns

```
Text file contents.
```

---

## JsonLoader

### Description

Loads JSON documents.

### Method

```python
load(file_path: str) -> str
```

### Returns

```
JSON content as text.
```

---

## OCRProcessor

### Description

Extracts text from images using OCR.

### Method

```python
extract(file_path: str) -> str
```

### Supported Formats

- PNG
- JPG
- JPEG
- BMP
- TIFF

---

## MetadataExtractor

### Description

Extracts metadata from files.

### Method

```python
extract(file_path: str) -> dict
```

### Returns

```python
{
    "file_name": "...",
    "file_size": "...",
    "extension": "...",
    "language": "..."
}
```

---

# Preprocessing Module

## TextCleaner

### Description

Cleans extracted text.

### Method

```python
clean(text: str) -> str
```

### Operations

- Remove extra spaces
- Remove blank lines
- Clean unwanted characters

---

## TextNormalizer

### Description

Normalizes text.

### Method

```python
normalize(text: str) -> str
```

### Operations

- Lowercase conversion
- Unicode normalization
- Standardized spacing

---

## LanguageDetector

### Description

Detects the language of the document.

### Method

```python
detect(text: str) -> str
```

### Returns

Example:

```
English
French
German
```

---

## DocumentValidator

### Description

Validates extracted documents.

### Method

```python
validate(file_path: str, text: str)
```

### Returns

```python
(True, "Valid")
```

or

```python
(False, "Error Message")
```

---

# IngestionPipeline

### Description

Coordinates the complete document ingestion process.

### Method

```python
run(file_path: str)
```

### Workflow

```
Input File
      │
      ▼
Loader
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
```

### Returns

A `Document` object containing:

- Source Path
- Extracted Text
- Clean Text
- Metadata
- Language
- Validation Status
- Error Message

---

# Main Application

### File

```
src/main.py
```

### Run

```bash
python -m src.main
```

---

# Testing

Run all unit tests:

```bash
python -m pytest
```

Expected output:

```
7 passed
```

---

# Supported File Types

| Extension | Supported |
|-----------|-----------|
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

# Output Locations

Processed text:

```
data/processed/
```

Metadata:

```
data/metadata/
```

---

# Version

**Version:** 1.0.0 