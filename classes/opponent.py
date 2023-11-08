import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Opponent:
    def __init__(self, name, dialogue, solution, health, location_id, id=None):
        self.name = name
        self.dialogue = dialogue
        self.solution = solution #add properties
        self.health = health #add properties
        self.location_id = location_id #add properties

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and not hasattr(self, 'name'):
            self._name = new_name
        else:
            raise Exception("Name must be string and cannot be reset")

    @property
    def dialogue(self):
        return self._dialogue
    @dialogue.setter
    def dialogue(self, new_dialogue):
        if isinstance(new_dialogue, str) and not hasattr(self, 'dialogue'):
            self._dialogue = new_dialogue
        else:
            raise Exception("Dialogue must be string and cannot be reset")

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS opponents (
            id INTEGER PRIMARY KEY,
            name TEXT,
            dialogue TEXT,
            solution TEXT,
            health INTEGER,
            location_id INTEGER)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS opponents
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO opponents (name, dialogue, solution, health, location_id)
            VALUES (?, ?, ?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.dialogue, self.solution, self.health, self.location_id))
        CONN.commit()

    @classmethod
    def create(cls, name, dialogue, solution, health, location_id):
        opponent = cls(name, dialogue, solution, health, location_id)
        opponent.save()
        return opponent
