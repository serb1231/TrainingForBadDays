import random
import time
from secrets import randbelow
import logging
logger = logging.getLogger(__name__)

class AIMock:
    def __init__(self):
        pass

    def acceptMessage(self, messages : list[dict[str, str]]):
        time.sleep(random.randint(1, 5))
        logger.debug(f"AI accepted message: {messages[-1]["content"]}")
        # return mock string
        return f"Mock AI Response: {messages[-1]["content"]}"