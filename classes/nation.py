import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Nation:
    def __init__(self, name, description, category, id=None):
        self.name = name
        self.description = description
        self.category = category #add properties

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
    def description(self):
        return self._description
    @description.setter
    def description(self, new_description):
        if isinstance(new_description, str) and not hasattr(self, 'description'):
            self._description = new_description
        else:
            raise Exception("Description must be string and cannot be reset")

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS nations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            description TEXT,
            category TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS nations
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO nations (name, description, category)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self.name, self.description, self.category))
        CONN.commit()

    @classmethod
    def create(cls, name, description, category):
        nation = cls(name, description, category)
        nation.save()
        return nation
