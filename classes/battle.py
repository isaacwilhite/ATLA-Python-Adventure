import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Battle():
    def __init__(self, player_id, opponent_id, challenge_id, status, id=None):
        self.player_id = player_id
        self.opponent_id = opponent_id
        self.challenge_id = challenge_id
        self.status = status
        self.id = id

    def start_battle(self, player, map_location):
        #what opponents are available on the map and if they have battled
        available_opponents = self.available_opponents(map_location, player)

        #!Battle Loop
        for opponent in available_opponents:
            battle_result = self.battle(player, opponent)

            if battle_result == "win":
                #!update status to win in db
                #~add new skill to Abilities Class (existing function)

            elif battle_result == "lose":
                from player import Player
                player.faint()
                #!reset location
            if battle_result == "retreat":
                break
                #! use function that reset_map() takes you back to the beginning

    def available_opponents(self, map_location, player):
        #! pass in a map_location and player progress (which battles are lost (0))
        #!return list of available opponents
        pass

    def battle(self, player, opponent):
        #! battle logic, take turns, return "win", "lose", "retreat"
        pass

    #~~~~~~~~~~~~~~~~~~~~~~CRUD~~~~~~~~~~~~~~~~~~~
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS battles (
                id INTEGER PRIMARY KEY,
                player_id INTEGER,
                opponent_id INTEGER,
                status INTEGER,
                FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,
                FOREIGN KEY (opponent_id) REFERENCES opponents(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS battles
        """
        CURSOR.execute(sql)
        CONN.commit()

    def add_battle(self, player_id, opponent_id, status):
        sql = """
            INSERT INTO battles (player_id, opponent_id, status)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (player_id, opponent_id, status))
        CONN.commit()

    def update_battle_status(self, status):
        sql = """
            UPDATE battles
            SET status = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (status,))
        CONN.commit()
