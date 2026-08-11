from pathlib import Path
from uuid import uuid4

from langchain_text_splitters import (
    RecursiveCharacterTextSplitter
)

from src.chunking.chunk_models import Chunk


class RecursiveChunker:
    """
    Splits document text into overlapping chunks.
    """

    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200

    @staticmethod
    def split(document):

        splitter = RecursiveCharacterTextSplitter(

            chunk_size=RecursiveChunker.CHUNK_SIZE,

            chunk_overlap=RecursiveChunker.CHUNK_OVERLAP,

            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

        pieces = splitter.split_text(document.clean_text)

        chunks = []

        for index, piece in enumerate(pieces):

            chunk = Chunk(

                chunk_id=str(uuid4()),

                document_name=document.metadata.get(
                        "filename",
                        Path(document.source_path).name
                    ),

                page_number=1,

                chunk_index=index,

                text=piece,

                character_count=len(piece),

                metadata=document.metadata

            )

            chunks.append(chunk)

        return chunks