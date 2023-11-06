import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Skill:
  def __init__(self, name, description, point_cost):
    self.name = name
    self.description = description
    self.point_cost = point_cost

  @property
  def name(self):
