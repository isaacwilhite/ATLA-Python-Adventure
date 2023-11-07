import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Abilities:
    def __init__(self, player_id, skill_id):
        self.player_id = player_id
        self.skill_id = skill_id
        self.skills = []

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
                FOREIGN KEY (player_id) REFERENCES player(id) ON DELETE CASCADE,
                FOREIGN KEY (skill_id) REFERENCES skill(id)
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
    def find_by_player_skill(cls, player_id, skill_id):
        ##return abilities instance having the player_id and skill_id
        sql = """
            SELECT * FROM abilities WHERE player_id = ? AND skill_id = ?
        """
        CURSOR.execute(sql, (player_id, skill_id))
        record = CURSOR.fetchone()

        if record:
            return cls(*record)
        else:
            return None


    ##add to the db
    @classmethod
    def create_db_instance(cls, player_id, skill_id):
        #check if record exists
        existing_ability = cls.find_by_player_skill(player_id, skill_id)

        if existing_ability:
            raise Exception("You already have this ability")

        ability = cls(player_id, skill_id)
        ability.save()
        return ability

    ##get all the skills the player has by name
    @classmethod
    def get_skills_for_player(cls, player_id):
        sql = """
            SELECT skill_id FROM abilities WHERE player_id = ?
        """
        CURSOR.execute(sql, (player_id,))
        skill_ids = CURSOR.fetchall()

        skill_list = []
        for skill_id in skill_ids:
            sql = """
                SELECT name from skill WHERE id = ?
            """
            CURSOR.execute(sql, (skill_id[0],))
            skill_name = CURSOR.fetchone()
            if skill_name:
                skill_list.append(skill_name[0])

        return skill_list
###Usage
# player_id = 1  # Replace with the actual player's ID
# skills = Abilities.get_skills_for_player(player_id)
# print("Skills:", skills)
