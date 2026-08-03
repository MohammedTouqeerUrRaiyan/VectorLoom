from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            cls._model = SentenceTransformer(
                "BAAI/bge-small-en-v1.5"
            )

        return cls._model