from collections import defaultdict
from datetime import datetime

from src.memory.conversation import Message


class MemoryService:

    _memory = defaultdict(list)

    MAX_HISTORY = 10

    @classmethod
    def add_user_message(
        cls,
        session_id: str,
        content: str
    ):

        cls._memory[session_id].append(

            Message(

                role="user",

                content=content,

                timestamp=datetime.utcnow()

            )

        )

        cls._trim(session_id)

    @classmethod
    def add_assistant_message(
        cls,
        session_id: str,
        content: str
    ):

        cls._memory[session_id].append(

            Message(

                role="assistant",

                content=content,

                timestamp=datetime.utcnow()

            )

        )

        cls._trim(session_id)

    @classmethod
    def history(
        cls,
        session_id: str
    ):

        return cls._memory[session_id]

    @classmethod
    def clear(
        cls,
        session_id: str
    ):

        cls._memory.pop(session_id, None)

    @classmethod
    def _trim(
        cls,
        session_id: str
    ):

        if len(cls._memory[session_id]) > cls.MAX_HISTORY:

            cls._memory[session_id] = cls._memory[session_id][-cls.MAX_HISTORY:]