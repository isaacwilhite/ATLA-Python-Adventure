import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

import sqlite3

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Location:
    def __init__(self, name, description, category, id=None):
        self._name = name
        self._description = description
        self.category = category #! Need to safeguard this entry
        self.id = id
        self.directions = {} #! Need to safeguard this entry

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if isinstance(new_name, str) and not hasattr(self, '_name'):
            self._name = new_name
        else:
            raise ValueError("Name must be a string and cannot be reset")

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, new_description):
        if isinstance(new_description, str) and not hasattr(self, '_description'):
            self._description = new_description
        else:
            raise ValueError("Description must be a string and cannot be reset")

    @classmethod
    def create_table(cls):
        sql = """
        CREATE TABLE IF NOT EXISTS locations (
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
            DROP TABLE IF EXISTS locations
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO locations (name, description, category)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (self._name, self._description, self.category))
        CONN.commit()

    @classmethod
    def create(cls, name, description, category):
        location = cls(name, description, category)
        location.save()
        return location

    @classmethod
    def load_locations(cls, map_instance):
        locations = []
        sql = "SELECT * FROM locations"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        for row in rows:
            location = cls(name=row[1], description=row[2], category=row[3], id=row[0])
            # print(f"Loading location: {location.id}, Directions: {map_instance.directions.get(location.id, {})}")
            location.directions = map_instance.directions.get(location.id, {})
            locations.append(location)
        return locations

    def retrieve_category(self):
        sql = """
            SELECT category FROM locations
            WHERE id = ?
        """
        category_list = CURSOR.execute(sql, (self.id,)).fetchone()
        return category_list[0] if category_list else None

    #~~~~~~~~~associations
    def retrieve_opponent(self):
        from classes.opponent import Opponent
        opponents = Opponent.all()
        # import ipdb; ipdb.set_trace()
        for opponent in opponents:
            if opponent.location_id == self.id:
                return opponent
        return None
# from map import Map
# map_instance = Map()

# map_instance.add_connection(1, "West", 2)
# map_instance.add_connection(2, "East", 3)
# map_instance.add_connection(3, "South", 4)
# map_instance.add_connection(4, "Southeast", 11)
# map_instance.add_connection(11, "South", 13)
# map_instance.add_connection(13, "North", 12)
# map_instance.add_connection(12, "Southeast", 14)
# map_instance.add_connection(14, "North", 7)
# map_instance.add_connection(7, "Northeast", 10)
# map_instance.add_connection(10, "Southwest", 9)
# map_instance.add_connection(9, "North", 8)
# map_instance.add_connection(8, "West", 15)

# locations = Location.load_locations(map_instance)
# current_location = locations[0]
# current_location.retrieve_opponent()
