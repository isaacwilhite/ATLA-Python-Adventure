import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Abilities:
    def __init__(self, player_id, skill_id):
        self.player_id = player_id
        self.skill_id = skill_id

    @property
    def player_id(self):
        return self._player_id
    @player_id.setter
    def player_id(self, player_id):
        if isinstance(player_id, int):
            self._player_id = player_id
        else:
            raise TypeError("Player ID must be an integer")

    @property
    def skill_id(self):
        return self._skill_id
    @skill_id.setter
    def skill_id(self, skill_id):
        if isinstance(skill_id, int):
            self._skill_id = skill_id
        else:
            raise TypeError("Skill ID must be an integer")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS abilities (
                id INTEGER PRIMARY KEY,
                player_id INTEGER,
                skill_id INTEGER
                FOREIGN KEY (player_id, skill_id) REFERENCES player(id), skill(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS abilities
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO abilities (player_id, skill_id)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.player_id, self.skill_id))
        CONN.commit()

    @classmethod
    def create(cls, player_id, skill_id):
        ability = cls(player_id, skill_id)
        ability.save()
        return ability
