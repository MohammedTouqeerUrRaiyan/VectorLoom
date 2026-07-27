from pathlib import Path
import shutil
from fastapi import UploadFile

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class FileService:

    @staticmethod
    async def save(file: UploadFile):

        destination = UPLOAD_DIR / file.filename

        with open(destination, "wb") as buffer:

            shutil.copyfileobj(file.file, buffer)

        return destination

    @staticmethod
    def delete(path: Path):

        if path.exists():
            path.unlink()

    @staticmethod
    def exists(path: Path):

        return path.exists()