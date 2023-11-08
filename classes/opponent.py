import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Opponent:
    def __init__(self, name, dialogue, solution, health, location_id, id=None):
        self._name = name
        self._dialogue = dialogue
        self._solution = solution  # Added this line
        self.health = health
        self.location_id = location_id
        self.id = id

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and not hasattr(self, '_name'):
            self._name = new_name
        else:
            raise ValueError("Name must be a string and cannot be reset")

    @property
    def dialogue(self):
        return self._dialogue
    
    @dialogue.setter
    def dialogue(self, new_dialogue):
        if isinstance(new_dialogue, str) and not hasattr(self, '_dialogue'):
            self._dialogue = new_dialogue
        else:
            raise ValueError("Dialogue must be a string and cannot be reset")

    @property
    def solution(self):
        return self._solution
    
    @solution.setter
    def solution(self, new_solution):
        if isinstance(new_solution, str) and not hasattr(self, '_solution'):
            self._solution = new_solution
        else:
            raise ValueError("Solution must be a string and cannot be reset")

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

    @classmethod
    def all(cls):
        sql = """
            SELECT *
            FROM opponents
        """
        opponents_data = CURSOR.execute(sql).fetchall()
        CONN.commit()
        return [cls(*data) for data in opponents_data]