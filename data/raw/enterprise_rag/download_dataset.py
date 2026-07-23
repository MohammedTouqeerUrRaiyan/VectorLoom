from datasets import load_dataset
import os

# ==========================================================
# Configuration
# ==========================================================

DATASET_NAME = "SJChen02/EnterpriseRAG-Bench"
OUTPUT_DIR = "data/raw/enterprise_rag"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==========================================================
# Download Documents
# ==========================================================

print("=" * 70)
print("Downloading EnterpriseRAG-Bench Documents")
print("=" * 70)

documents = load_dataset(
    DATASET_NAME,
    "documents"
)

print(documents)

doc_split = list(documents.keys())[0]
document_dataset = documents[doc_split]

print(f"\nUsing split : {doc_split}")
print(f"Total Documents : {len(document_dataset):,}")

sample_size = min(1000, len(document_dataset))

documents_sample = document_dataset.select(
    range(sample_size)
)

documents_sample.to_json(
    os.path.join(
        OUTPUT_DIR,
        "documents_sample.json"
    ),
    orient="records",
    lines=True
)

print("✓ Saved documents_sample.json")

# ==========================================================
# Download Questions
# ==========================================================

print("\n" + "=" * 70)
print("Downloading EnterpriseRAG-Bench Questions")
print("=" * 70)

questions = load_dataset(
    DATASET_NAME,
    "questions"
)

print(questions)

question_split = list(questions.keys())[0]
question_dataset = questions[question_split]

print(f"\nUsing split : {question_split}")
print(f"Total Questions : {len(question_dataset):,}")

sample_size = min(1000, len(question_dataset))

questions_sample = question_dataset.select(
    range(sample_size)
)

questions_sample.to_json(
    os.path.join(
        OUTPUT_DIR,
        "questions_sample.json"
    ),
    orient="records",
    lines=True
)

print("✓ Saved questions_sample.json")

# ==========================================================
# Preview Dataset
# ==========================================================

print("\n" + "=" * 70)
print("Sample Document")
print("=" * 70)

print(document_dataset[0])

print("\n" + "=" * 70)
print("Sample Question")
print("=" * 70)

print(question_dataset[0])

# ==========================================================
# Completed
# ==========================================================

print("\n" + "=" * 70)
print("EnterpriseRAG-Bench Download Completed Successfully")
print("=" * 70)

print(f"Files saved to:\n{OUTPUT_DIR}")