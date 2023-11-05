#lib/config.py

import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Player:

  def __init__(self, )
