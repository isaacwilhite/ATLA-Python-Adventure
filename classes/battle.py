import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Battle():
    def __init__(self, player_id, opponent_id, challenge_id, status, id=None):
        self.player_id = player_id
        self.opponent_id = opponent_id
        self.challenge_id = challenge_id
        self.status = status
