import logging
logger = logging.getLogger(__name__)

class ContextManager:
    def __init__(self, max_nr_messages):
        self.max_nr_messages = max_nr_messages

    def truncate(self, conversation_history : list[dict[str, str]]) -> list[dict[str, str]]:
        logger.debug(f"truncated and got the entries: {conversation_history[-5:]}")
        return conversation_history[-5:]