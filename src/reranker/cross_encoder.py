from sentence_transformers import CrossEncoder


class CrossEncoderModel:
    """
    Singleton wrapper around the CrossEncoder model.
    """

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            cls._model = CrossEncoder(
                "cross-encoder/ms-marco-MiniLM-L-6-v2"
            )

        return cls._model