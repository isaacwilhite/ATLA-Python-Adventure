import click
import sys
from classes.player import *
from classes.abilities import *
from classes.map import *
from classes.location import *
from classes.battle import *
from helpers import (
    create_new_user,
    login_existing_user,
    remove_player_from_db,
    check_quit,
    load_locations,
    display_location,
    move,
    __init__
)

def welcome():
    file_path = 'txt/intro.txt'

    with open(file_path, 'r') as file:
        content = file.read()
        print(content)
##prompt user for a choice

def main_menu():
    while True:
        click.echo("Main Menu:")
        click.echo("1. Start a New Game")
        click.echo("2. Load a Saved Game")
        click.echo("3. Remove Player")
        click.echo("4. Quit")
        choice = click.prompt("Choose an option)", type=click.Choice(['1', '2', '3', '4']))

        if choice == '1':
            player = create_new_user()
            adventure(player)
            break
        elif choice == '2':
            player = login_existing_user()
            adventure(player)
        elif choice == '3':
            remove_player_from_db()
        elif choice == '4':
            check_quit("quit")
            return
        else:
            click.echo("Invalid choice. Please enter '1', '2', '3', or '4'.")

def adventure(player):
    while True:

        click.echo("ATLA Menu:")
        click.echo("1. Start Game")
        click.echo("2. Check Skills")
        click.echo("3. Check Health")
        click.echo("4. Quit Adventure")

        adventure_choice = click.prompt("Choose an option (1/2/3/4)", type=click.Choice(['1', '2', '3', '4']))

        if adventure_choice == '1':
            enter_map(player)
            #!battle logic
        if adventure_choice == '2':
            skills = Abilities.get_skills_for_player(player.id)
            click.echo(f"Your skills: {', '.join(skills)}")
        elif adventure_choice == '3':
            click.echo(f"Your Health: {player.health}")
        elif adventure_choice == '4':
            click.echo("Returning to the Main Menu...")
            return  # Return to the main menu
        else:
            click.echo("Invalid choice. Please enter '1', '2', '3', or '4'.")

def enter_map(player):
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

    opponent_at_location = current_location.retrieve_opponent()
    current_category = current_location.retrieve_category()
    if opponent_at_location == None:
        click.echo("Continue exploring to find an opponent")
    elif opponent_at_location:
        existing_battle_records = Battle.all_battles()
        for battle_record in existing_battle_records:
            if battle_record.player_id == player.id and battle_record.opponent_id == opponent_at_location.id:
                if battle_record.status == 0:
                    battle = Battle.get_battle_by_id(battle_record.id)
                    battle.start_battle(player, opponent_at_location, current_category)
                    break
                elif battle_record.status == 1:
                    click.echo("You have already defeated this opponent")
        #!no existing battle records
        if len(existing_battle_records) == 0:
            new_battle = Battle(player.id, opponent_at_location.id)
            #!add battle record to database
            new_battle.add_battle(player.id, opponent_at_location, 0)
            #!start the battle
            new_battle.start_battle(player, opponent_at_location, current_category)


    while True:
        display_location(current_location, locations)
        direction = input("\nEnter the direction to move (q to quit): ").capitalize()

        if direction == 'Q':
            print("Exiting the map. Goodbye!")
            return

        connected_location_id = map_instance.get_connected_location_id(current_location.id, direction.capitalize())

        if connected_location_id is not None:
            current_location = next((loc for loc in locations if loc.id == connected_location_id), None)
            if current_location is None:
                print("Error: Invalid connected location ID.")
                break
        else:
            print("Error: Invalid direction. Please choose a valid direction.")


if __name__ == "__main__":
    welcome()
    main_menu()
