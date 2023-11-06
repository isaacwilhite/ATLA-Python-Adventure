import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Nation:
    def __init__(self, name, description, category, id=None):
        self.name = name
        self.description = description
        self.category = category #add properties

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY
            name TEXT,
            description TEXT,
            category TEXT
        )
        """
        CURSOR.execute(sql)
        CONN.commit()
