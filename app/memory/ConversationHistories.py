from threading import Lock

class ConversationHistories:
    def __init__(self):
        self.conversations  : dict[str, list[dict[str, str]]]= {}
        self.per_user_lock : dict[str, Lock] = {}
        self.dict_lock = Lock()

    def create_entry(self, user : str):
        with self.dict_lock:
            self.conversations[user] = []
            self.per_user_lock[user] = Lock()

    def append(self, user : str, conversation : dict[str, str]):
        with self.per_user_lock[user]:
            self.conversations[user].append(conversation)


    def get_all(self, user: str) -> list[dict[str, str]]:
        with self.per_user_lock[user]:
            conversation = self.conversations[user]
            return list(conversation)

    def pop(self, user: str):
        with self.dict_lock:
            self.conversations.pop(user)
            self.per_user_lock.pop(user)

    def verify_existence_and_insert(self, user: str):
        with self.dict_lock:
            if user not in self.conversations:
                self.conversations[user] = []
                self.per_user_lock[user] = Lock()

    def verify_existence(self, user: str):
        with self.dict_lock:
            result = True
            if user not in self.conversations:
                result = False
            return result