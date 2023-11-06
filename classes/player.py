import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Player:

    def __init__(self, username="", health = 10, id=None):
        self.username = username.lower()
        self.health = health
        self.points = 0
        self.id = id

    @property
    def username(self):
        return self._username
    @username.setter
    def username(self, new_user):
        if not isinstance(new_user, str):
            raise TypeError("Username must be a string")
        elif len(new_user) not in range(1, 11):
            raise Exception("Username should be between 1 and 10 characters")
        elif not hasattr(self, "username"):
            raise Exception("Username cannot be reset")
        else:
            self._username = new_user

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                username TEXT,
                health INTEGER,
                points INTEGER
            )
        """
        CURSOR.execute(sql)
        CONN.commit()
        CONN.close()
