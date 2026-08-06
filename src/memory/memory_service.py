from collections import defaultdict

from src.memory.conversation import Message


class MemoryService:
    """
    Simple in-memory conversation store.

    Can later be replaced by:
    - Redis
    - PostgreSQL
    - MongoDB
    """

    MAX_HISTORY = 10

    _memory = defaultdict(list)

    @classmethod
    def add_user_message(cls, session_id: str, message: str):
        cls._memory[session_id].append(
            Message(
                role="user",
                content=message
            )
        )

        cls._trim(session_id)

    @classmethod
    def add_assistant_message(cls, session_id: str, message: str):
        cls._memory[session_id].append(
            Message(
                role="assistant",
                content=message
            )
        )

        cls._trim(session_id)

    @classmethod
    def get_history(cls, session_id: str):

        return cls._memory[session_id]

    @classmethod
    def clear(cls, session_id: str):

        cls._memory.pop(session_id, None)

    @classmethod
    def _trim(cls, session_id: str):

        if len(cls._memory[session_id]) > cls.MAX_HISTORY:

            cls._memory[session_id] = cls._memory[session_id][-cls.MAX_HISTORY:]