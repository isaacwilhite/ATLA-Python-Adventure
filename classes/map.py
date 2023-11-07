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

# Add connections between locations
map_instance.add_connection(1, "North", 2)
map_instance.add_connection(3, "North", 2)
map_instance.add_connection(2, "South", 3)
map_instance.add_connection(4, "South", 3)
map_instance.add_connection(6, "East", 4)
map_instance.add_connection(3, "East", 4)
map_instance.add_connection(7, "West", 8)
map_instance.add_connection(9, "West", 8)
map_instance.add_connection(8, "Northeast", 9)
map_instance.add_connection(10, "Northeast", 9)
map_instance.add_connection(9, "Southeast", 10)



# Get the connected location ID
connected_location_id = map_instance.get_connected_location_id(1, "north")
print(f"The location connected to the north of location 1 is location {connected_location_id}")