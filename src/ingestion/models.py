from pydantic import BaseModel


class Document(BaseModel):

    filename: str

    extension: str

    pages: int

    characters: int

    text: str

    metadata: dict