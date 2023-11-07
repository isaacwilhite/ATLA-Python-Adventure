from classes import *

def helper_1():
    print("Performing useful function#1.")


def exit_program():
    print("Thanks for playing Avatar!")
    exit()

def __init__(self, map_instance):
        self.map_instance = map_instance
        self.current_location_id = 1  # Assuming starting location ID is 1

def move(self, direction):
    # Retrieve the connected location name based on the current location and direction
    connected_location_name = self.map_instance.get_connected_location_name(self.current_location_id, direction)

    if connected_location_name:
        print(f"You are moving {direction} to {connected_location_name}.")
        # Update the current location for future moves
        self.current_location_id = self.map_instance.get_location_id_by_name(connected_location_name)
    else:
        print(f"There is no connection {direction} from your current location.")