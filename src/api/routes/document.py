from pathlib import Path

import chromadb
from fastapi import APIRouter, HTTPException

from src.config.settings import Settings

router = APIRouter(prefix="/documents", tags=["Documents"])


client = chromadb.PersistentClient(
    path=Settings.CHROMA_PATH
)

collection = client.get_collection(
    Settings.COLLECTION_NAME
)

@router.get("/")
async def list_documents():

    data = collection.get(
        include=["metadatas"]
    )

    documents = {}

    for meta in data["metadatas"]:

        name = meta["document_name"]

        if name not in documents:

            documents[name] = {
                "name": name,
                "pages": set(),
                "chunks": 0
            }

        documents[name]["pages"].add(
            meta["page"]
        )

        documents[name]["chunks"] += 1

    response = []

    for doc in documents.values():

        response.append(

            {
                "name": doc["name"],
                "pages": len(doc["pages"]),
                "chunks": doc["chunks"]
            }

        )

    return response

@router.delete("/{document_name}")
async def delete_document(
    document_name: str
):

    data = collection.get(
        include=["metadatas"]
    )

    ids_to_delete = []

    for idx, meta in zip(
        data["ids"],
        data["metadatas"]
    ):

        if meta["document_name"] == document_name:

            ids_to_delete.append(idx)

    if not ids_to_delete:

        raise HTTPException(
            status_code=404,
            detail="Document not found."
        )

    collection.delete(
        ids=ids_to_delete
    )

    uploads = Path(
        Settings.UPLOAD_FOLDER
    )

    pdf = uploads / document_name

    if pdf.exists():

        pdf.unlink()

    return {

        "status": "success",

        "message": f"{document_name} deleted."

    }