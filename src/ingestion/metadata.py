from pathlib import Path
from datetime import datetime


class MetadataExtractor:
    """
    Extracts file metadata for any uploaded document.
    """

    @staticmethod
    def extract(file_path: Path) -> dict:
        """
        Returns metadata for the uploaded document.
        """

        stat = file_path.stat()

        return {
            "filename": file_path.name,
            "extension": file_path.suffix.lower(),
            "size_bytes": stat.st_size,
            "size_kb": round(stat.st_size / 1024, 2),
            "created_at": datetime.fromtimestamp(stat.st_ctime).isoformat(),
            "modified_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "parent_directory": str(file_path.parent),
            "absolute_path": str(file_path.resolve())
        }