import os
import json

from src.ingestion.pipeline import IngestionPipeline


def main():

    pipeline = IngestionPipeline()

    RAW_DATA_DIR = "data/raw"
    OUTPUT_DIR = "data/processed"
    METADATA_DIR = "data/metadata"

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(METADATA_DIR, exist_ok=True)

    processed = 25

    for root, dirs, files in os.walk(RAW_DATA_DIR):

        for file in files:

            file_path = os.path.join(root, file)

            print(f"\nProcessing: {file_path}")

            try:
                document = pipeline.run(file_path)

                if not document.valid:
                    print(f"Skipped: {document.error}")
                    continue

                filename = os.path.splitext(file)[0]

                # Save cleaned text
                output_file = os.path.join(
                    OUTPUT_DIR,
                    filename + ".txt"
                )

                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(document.clean_text)

                # Save metadata
                metadata_file = os.path.join(
                    METADATA_DIR,
                    filename + ".json"
                )

                with open(metadata_file, "w", encoding="utf-8") as f:
                    json.dump(
                        document.metadata,
                        f,
                        indent=4,
                        ensure_ascii=False
                    )

                processed += 1
                print(f"Done: {file}")

            except Exception as e:
                print(f"Error processing {file}: {e}")

    print("\n==============================")
    print(f"Processed Documents: {processed}")
    print("==============================")


if __name__ == "__main__":
    main()