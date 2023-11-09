import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Map:
    def __init__(self):
        self.directions = {}

    def add_connection(self, location_id, direction, connected_location_id):
        if location_id not in self.directions:
            self.directions[location_id] = {}
        self.directions[location_id][direction] = connected_location_id

    def get_connected_location_id(self, location_id, direction):
        return self.directions.get(location_id, {}).get(direction)

map_instance = Map()





# Get the connected location ID
connected_location_id = map_instance.get_connected_location_id(1, "north")
# print(f"The location connected to the north of location 1 is location {connected_location_id}")
