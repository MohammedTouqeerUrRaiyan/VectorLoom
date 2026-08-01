# User Guide

## Introduction

Welcome to **VectorLoom**.

VectorLoom is a document ingestion pipeline that extracts, cleans, validates, and processes documents from multiple file formats. The processed output is stored for AI and Retrieval-Augmented Generation (RAG) applications.

---

# Features

The system supports:

- PDF Documents
- Microsoft Word Documents (.docx)
- Text Files (.txt)
- JSON Files
- Image Files (OCR)

The pipeline automatically:

- Extracts text
- Cleans text
- Normalizes text
- Detects language
- Validates documents
- Extracts metadata
- Saves processed output

---

# Supported File Types

| File Type | Supported |
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
├── src/
│
├── tests/
│
└── docs/
```

---

# Installation

Install the required packages:

```bash
pip install -r requirements.txt
```

---

# Running the Project

Move to the project folder:

```bash
cd D:\vectorloom
```

Run the application:

```bash
python -m src.main
```

---

# Running Tests

Execute:

```bash
python -m pytest
```

Expected Output:

```
7 passed
```

---

# Input Files

Place supported input files inside:

```
data/input/
```

Example:

```
sample1.pdf
sample2.docx
sample3.txt
```

The raw dataset is stored in:

```
data/raw/
```

---

# Output Files

After processing, the project generates:

Processed text:

```
data/processed/
```

Metadata:

```
data/metadata/
```

---

# Example Output

```
Processing: data/raw/enterprise_rag/documents_sample.json

Done: documents_sample.json

Processing: data/raw/enterprise_rag/questions_sample.json

Done: questions_sample.json

Processed Documents: 27
```

---

# Troubleshooting

## ModuleNotFoundError

Run the project from the project root:

```bash
cd D:\vectorloom
python -m src.main
```

---

## File Not Found

Ensure that required input files exist in:

```
data/input/
```

---

## Test Failures

Run:

```bash
python -m pytest
```

Review the error messages and verify the required input files are present.

---

# Tips

- Keep source files in the correct folders.
- Run tests after making code changes.
- Review output files in `data/processed/` and `data/metadata/`.
- Update documentation whenever new features are added.

---

# Contact

For issues or improvements, contact the project maintainer or development team.