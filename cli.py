from helpers import (
    exit_program,
    helper_1
)

import os
import sqlite3
import subprocess

from classes.location import Location  
from classes.map import Map  

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()


def load_locations():
    locations = []
    sql = "SELECT * FROM locations"
    CURSOR.execute(sql)
    rows = CURSOR.fetchall()
    for row in rows:
        location = Location(name=row[1], description=row[2], category=row[3], id=row[0])
        locations.append(location)
    return locations

def display_location(location, locations):
    subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True) 
    print(f"Location: {location.name}")
    print(f"Description: {location.description}")
    print(f"Category: {location.category}")
    print("\nAvailable Directions:")
    for direction, connected_location_id in location.directions.items():
        connected_location = next((loc for loc in locations if loc.id == connected_location_id), None)
        print(f"{direction.capitalize()}: {connected_location.name if connected_location else 'Unknown'}")

def main():
    map_instance = Map()
    
    # Add connections between locations
    map_instance.add_connection(1, "West", 2)
    map_instance.add_connection(2, "East", 3)
    map_instance.add_connection(3, "South", 4)
    map_instance.add_connection(4, "Southeast", 11)
    map_instance.add_connection(11, "South", 13)
    map_instance.add_connection(13, "North", 12)
    map_instance.add_connection(12, "Southeast", 14)
    map_instance.add_connection(14, "North", 7)
    map_instance.add_connection(7, "Northeast", 10)
    map_instance.add_connection(10, "Southwest", 9)
    map_instance.add_connection(9, "North", 8)
    map_instance.add_connection(8, "West", 15)
    

    locations = Location.load_locations(map_instance)
    current_location = locations[0]  # Assuming the starting location is the first in the list

    while True:
        display_location(current_location, locations)
        direction = input("\nEnter the direction to move (q to quit): ").capitalize()

        if direction == 'Q':
            print("Exiting the map. Goodbye!")
            break

        connected_location_id = map_instance.get_connected_location_id(current_location.id, direction.capitalize())
        
        if connected_location_id is not None:
            current_location = next((loc for loc in locations if loc.id == connected_location_id), None)
            if current_location is None:
                print("Error: Invalid connected location ID.")
                break
        else:
            print("Error: Invalid direction. Please choose a valid direction.")


if __name__ == "__main__":
    main()
# def main():
#     while True:
#         menu()
#         choice = input("> ")
#         if choice == "0":
#             exit_program()
#         elif choice == "1":
#             helper_1()
#         else:
#             print("Invalid choice")


# def menu():
#     print("Please select an option:")
#     print("0. Exit the program")
#     print("1. Some useful function")


# if __name__ == "__main__":
#     main()
