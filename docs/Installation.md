# Installation Guide

## Introduction

This guide explains how to install and run the VectorLoom project on Windows.

---

# Prerequisites

Before installing, ensure you have:

- Python 3.10 or later
- Git (optional)
- Visual Studio Code
- Internet connection

---

# Clone the Project

```bash
git clone <repository-url>
cd vectorloom
```

Or open the existing project folder:

```
D:\vectorloom
```

---

# Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

Verify installation:

```bash
pip list
```

---

# Project Structure

```
vectorloom/
│
├── data/
├── docs/
├── models/
├── notebooks/
├── src/
├── tests/
├── requirements.txt
└── download_dataset.py
```

---

# Download Dataset

Run:

```bash
python download_dataset.py
```

The dataset will be stored in:

```
data/raw/enterprise_rag/
```

---

# Run Unit Tests

Execute:

```bash
python -m pytest
```

Expected Output:

```
7 passed
```

---

# Run the Application

Execute:

```bash
python -m src.main
```

Expected Output:

```
Processing: data/raw/enterprise_rag/documents_sample.json
Done: documents_sample.json

Processing: data/raw/enterprise_rag/questions_sample.json
Done: questions_sample.json

Processed Documents: 27
```

---

# Output Files

Processed text:

```
data/processed/
```

Metadata:

```
data/metadata/
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

## Missing File Error

Ensure the following folders exist:

```
data/input/
data/raw/
```

Verify that the required files are available.

---

## Run Tests Again

```bash
python -m pytest
```

---

# Installation Complete

The project is successfully installed when:

- Dependencies are installed.
- Dataset is downloaded.
- All tests pass.
- The application runs without errors.