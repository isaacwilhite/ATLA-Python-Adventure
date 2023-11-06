import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Opponent:
    def __init__(self, name, dialogue, solution, reward_id, nation_id id=None):
        self.name = name
        self.dialogue = dialogue
        self.solution = solution
        self.reward_id = reward_id
        self.nation_id = nation_id #add properties

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS skills (
            id INTEGER PRIMARY KEY
            name TEXT,
            dialogue TEXT,
            solution TEXT,
            reward_id INTEGER,
            nation_id INTEGER
        )
        """
        CURSOR.execute(sql)
        CONN.commit()
