import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Skill:
    def __init__(self, name, description, point_cost, id=None):
        self.name = name
        self.description = description #need description property
        self.point_cost = point_cost #need point-cost property
        self.id = id

    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and not hasattr(self, 'name'):
            self._name = new_name
        else:
            raise Exception("Name must be a string and cannot be reset")

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY
            name TEXT,
            description TEXT,
            point_cost INTEGER
        )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS skills
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO skills (name, description, point_cost)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.description, self.point_cost))
        CONN.commit()

    @classmethod
    def create(cls, name, description, point_cost):
        skill = cls(name, description, point_cost)
        skill.save()
        return skill
