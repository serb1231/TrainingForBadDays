from threading import Lock

class ConversationHistories:
    def __init__(self):
        self.conversations  : dict[str, list[dict[str, str]]]= {}
        self.per_user_lock : dict[str, Lock] = {}
        self.dict_lock = Lock()

    def create_entry(self, user : str):
        self.dict_lock.acquire()

        try:
            self.conversations[user] = []
            self.per_user_lock[user] = Lock()
        finally:
            self.dict_lock.release()

    def append(self, user : str, conversation : dict[str, str]):
        self.per_user_lock[user].acquire()
        try:
            self.conversations[user].append(conversation)
        finally:
            self.per_user_lock[user].release()


    def get_all(self, user: str) -> list[dict[str, str]]:
        self.per_user_lock[user].acquire()
        try:
            conversation = self.conversations[user]
        finally:
            self.per_user_lock[user].release()

        return conversation

    def pop(self, user: str):
        self.per_user_lock[user].acquire()
        try:
            self.conversations.pop(user)
        finally:
            self.per_user_lock[user].release()

    def verify_existence_and_insert(self, user: str):
        self.dict_lock.acquire()

        try:
            if user not in self.conversations:
                self.conversations[user] = []
                self.per_user_lock[user] = Lock()
        finally:
            self.dict_lock.release()

    def verify_existence(self, user: str):
        self.dict_lock.acquire()
        result = True
        try:
            if user not in self.conversations:
                result = False
        finally:
            self.dict_lock.release()
        return result