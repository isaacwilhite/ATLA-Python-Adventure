import click
from classes.player import *
import sys
from classes.location import *
import subprocess
import os
from classes.abilities import *
from rich.console import Console

console = Console()

ABILITY_NUMBER = [1,7,13,19]

def create_new_user():
    click.echo("Welcome, new Avatar! You can create your username now.")
    username = click.prompt("Please input your username", type=str).lower()
    if username == 'quit':
        check_quit(username)

    existing_player = Player.find_by_username(username)
    if existing_player:
        click.echo("User already exists. Would you like to log in instead? (yes/no)")
        while True:
            choice = click.prompt("Log in instead?", type=click.Choice(['yes', 'no']))
            if choice == 'yes':
                return login_existing_user()
            elif choice == 'no':
                click.echo("Please choose a different username")
            elif choice == "quit":
                check_quit(choice)
            else:
                click.echo("Invalid choice. Please enter 'yes' or 'no'.")
    else:
        new_player = Player(username=username)
        new_player.save()

        new_player = Player.find_by_username(username) #!new code added/must retrieve from database

        for number in ABILITY_NUMBER:
            Abilities.create_db_instance(new_player.id, number)
        for number in range(25, 49):
            Abilities.create_db_instance(new_player.id, number)
        return new_player

def login_existing_user():
    while True:
        username = click.prompt("Please input your username", type=str).strip().lower()
        #check if they wanna quit
        if username == 'quit':
            check_quit(username)
            return
        existing_player = Player.find_by_username(username)
        if existing_player:
            click.echo(f"Welcome back, {username}! You can resume your journey as an Avatar.")
            return existing_player
        else:
            click.echo("We cannot find your username. Please try again or type 'quit' to exit.")

##delete player from database
def remove_player_from_db():
    username = click.prompt("Please input your username to delete your player", type=str).lower().strip()
    player = Player.find_by_username(username)

    while True:
        if player:
            confirm = click.prompt("Are you sure you want to delete your player? The four nations need your help!", type=click.Choice(['yes', 'no']))
            if confirm == 'yes':
                player.delete_player() #removes player from db and cascades removal of abilities
                click.echo("Player data deleted sucessfully")
                break
            elif confirm == "no":
                click.echo("Player data was not deleted")
                break
            else:
                click.echo("Invalid choice. Please enter 'yes' or 'no'.")
        else:
            click.echo("Player not found. Please check your username.")

#~~~~~~~~~~~~~~~~~~~Map Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
    # subprocess.run('clear' if os.name == 'posix' else 'cls', shell=True)
    if location.category == "air":
        console.print(f"Location: {location.name}", style="#dc8c24")
        console.print(f"Description: {location.description}", style="#dc8c24")
        console.print(f"Category: {location.category}", style="#dc8c24")
        console.print("\nAvailable Directions:", style="#dc8c24")
    elif location.category == "fire":
        console.print(f"Location: {location.name}", style="#890E05")
        console.print(f"Description: {location.description}", style="#890E05")
        console.print(f"Category: {location.category}", style="#890E05")
        console.print("\nAvailable Directions:", style="#890E05")
    elif location.category == "water":
        console.print(f"Location: {location.name}", style="#66d7eb")
        console.print(f"Description: {location.description}", style="#66d7eb")
        console.print(f"Category: {location.category}", style="#66d7eb")
        console.print("\nAvailable Directions:", style="#66d7eb")
    elif location.category == "earth":
        console.print(f"Location: {location.name}", style="#295427")
        console.print(f"Description: {location.description}", style="#295427")
        console.print(f"Category: {location.category}", style="#295427")
        console.print("\nAvailable Directions:", style="#295427")
    for direction, connected_location_id in location.directions.items():
        connected_location = next((loc for loc in locations if loc.id == connected_location_id), None)
        print(f"{direction.capitalize()}: {connected_location.name if connected_location else 'Unknown'}")

def move(self, direction):
    # Retrieve the connected location name based on the current location and direction
    connected_location_name = self.map_instance.get_connected_location_name(self.current_location_id, direction)

    if connected_location_name:
        print(f"You are moving {direction} to {connected_location_name}.")
        # Update the current location for future moves
        self.current_location_id = self.map_instance.get_location_id_by_name(connected_location_name)
    else:
        print(f"There is no connection {direction} from your current location.")

def __init__(self, map_instance):
        self.map_instance = map_instance
        self.current_location_id = 1  # Assuming starting location ID is 1

##exit function
def check_quit(string):
    if string.lower() == "quit":
        click.echo("You have chosen to quit the game. What will we do without the Avatar! Please come back soon!")
    sys.exit()
