from pathlib import Path

import chromadb
from fastapi import APIRouter, HTTPException

from src.config.settings import settings


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


client = chromadb.PersistentClient(
    path=settings.CHROMA_PATH
)

collection = client.get_collection(
    settings.COLLECTION_NAME
)


@router.get("/")
async def list_documents():
    """
    List all documents currently stored in the vector database.
    """

    data = collection.get(
        include=["metadatas"]
    )

    documents = {}

    for meta in data.get("metadatas", []):
        if not meta:
            continue

        name = meta.get("document_name")

        if not name:
            continue

        if name not in documents:
            documents[name] = {
                "name": name,
                "pages": set(),
                "chunks": 0,
            }

        page = meta.get("page")

        if page is not None:
            documents[name]["pages"].add(page)

        documents[name]["chunks"] += 1

    response = []

    for doc in documents.values():
        response.append(
            {
                "name": doc["name"],
                "pages": len(doc["pages"]),
                "chunks": doc["chunks"],
            }
        )

    return response


@router.delete("/{document_name}")
async def delete_document(
    document_name: str,
):
    """
    Delete all chunks belonging to a document
    from the vector database and remove the uploaded file.
    """

    data = collection.get(
        include=["metadatas"]
    )

    ids_to_delete = []

    for idx, meta in zip(
        data.get("ids", []),
        data.get("metadatas", []),
    ):
        if not meta:
            continue

        if meta.get("document_name") == document_name:
            ids_to_delete.append(idx)

    if not ids_to_delete:
        raise HTTPException(
            status_code=404,
            detail="Document not found.",
        )

    collection.delete(
        ids=ids_to_delete
    )

    upload_folder = Path(
        settings.UPLOAD_FOLDER
    )

    uploaded_file = upload_folder / document_name

    if uploaded_file.exists():
        uploaded_file.unlink()

    return {
        "status": "success",
        "message": f"{document_name} deleted.",
        "chunks_deleted": len(ids_to_delete),
    }