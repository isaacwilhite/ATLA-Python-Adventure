import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Player:

    def __init__(self, username="", id=None):
        self.username = username.lower()
        self.health = 10
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
                health INTEGER)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS players
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO players (username, health)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.username, self.health))
        CONN.commit()

    @classmethod
    def create_new_player(cls, username, health):
        player = cls(username, health)
        player.save()
        return player

    ##find by username (used for login)
    @classmethod
    def find_by_username(cls, username):
        sql = """
            SELECT *
            FROM players
            WHERE username = ?
        """
        row = CURSOR.execute(sql, (username,)).fetchone()
        return cls(row[0], row[1]) if row else None
