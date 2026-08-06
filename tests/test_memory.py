from src.memory.memory_service import MemoryService


session = "demo"

MemoryService.add_user_message(
    session,
    "What is Salesforce?"
)

MemoryService.add_assistant_message(
    session,
    "Salesforce is a CRM platform."
)

MemoryService.add_user_message(
    session,
    "Who created it?"
)

history = MemoryService.get_history(session)

for message in history:
    print(f"{message.role}: {message.content}")