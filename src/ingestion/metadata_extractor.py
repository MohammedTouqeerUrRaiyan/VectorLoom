import os 
from datetime import datetime

class MetadataExtractor:
    def extract(self, file_path: str, extra: dict = None) -> dict:
        metadata = {}
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Extract basic file metadata
        metadata['file_name'] = os.path.basename(file_path)
        metadata['file_size'] = os.path.getsize(file_path)
        metadata['last_modified'] = datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat()

        # Include any extra metadata provided
        if extra:
            metadata.update(extra)

        return metadata