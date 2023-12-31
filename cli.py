import click
from rich.console import Console
from rich.theme import Theme
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
    __init__,
)
console = Console()
# custom_style_key =
#     [
#         "air": "dc8c24",
#         "fire": "#890e05",
#         "fire-bold": "bold reverse red"
#         "water":"66d7eb",
#         "earth": "#295427"
#     ]

def welcome():

    file_path = 'txt/intro.txt'

    with open(file_path, 'r') as file:
        content = file.read()
        click.echo()
        click.echo()
        console.print(content, style="#ed9609")
        click.echo()

def main_menu():
    while True:
        click.echo("Main Menu:")
        click.echo("1. Start a New Game")
        click.echo("2. Load a Saved Game")
        click.echo("3. Remove Player")
        click.echo("4. Quit")
        choice = click.prompt("Choose an option", type=click.Choice(['1', '2', '3', '4']))

        if choice == '1':
            player = create_new_user()
            adventure(player)
            console.print("Congratulations you are now a full-fledged Avatar!", style="bold bright_green")
            console.print("Get ready for Season 2 of ATLA Python Adventure Game!", style="bold bright_green")
            break
        elif choice == '2':

            player = login_existing_user()
            adventure(player)
            console.print("Congratulations you are now a full-fledged Avatar!", style="bold bright_green")
            console.print("Get ready for Season 2 of ATLA Python Adventure Game!", style="bold bright_green")
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
        if adventure_choice == '2':
            skills = Abilities.get_skills_for_player(player.id)
            console.print(f"Your skills: {', '.join(skills)}", style="cyan")
        elif adventure_choice == '3':
            console.print(f"Your Health: {player.health}", style = "bold bright_green")
            click.echo()
        elif adventure_choice == '4':
            click.echo("Returning to the Main Menu...")
            return
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
    map_instance.add_connection(15, "Northwest", 16)
    map_instance.add_connection(16, "East", 17)
    map_instance.add_connection(17, "Southwest", 18)
    map_instance.add_connection(18, "West", 19)

    locations = Location.load_locations(map_instance)
    current_location = locations[0]

    while True:
        display_location(current_location, locations)
        direction = input("\nEnter the direction to move (q to quit): ").capitalize()
        click.echo()

        if direction == 'Q':
            click.echo("Exiting the map. Goodbye!")
            return

        connected_location_id = map_instance.get_connected_location_id(current_location.id, direction)

        if connected_location_id is not None:
            new_location = next((loc for loc in locations if loc.id == connected_location_id), None)
            opponent_at_location = new_location.retrieve_opponent()
            current_category = new_location.retrieve_category()

            if opponent_at_location is not None:
                # Check for existing battle record
                existing_battle_records = Battle.all_battles()
                battle_found = False #!set flag
                for battle_record in existing_battle_records:
                    if battle_record.player_id == player.id and battle_record.opponent_id == opponent_at_location.id:
                        battle_found = True #!set flag
                        if battle_record.status == 0:
                            battle = Battle.get_battle_by_id(battle_record.id)
                            battle_outcome = battle.start_battle(player, opponent_at_location, current_category)

                            if battle_outcome == "win":
                                console.print("Congratulations! You won the battle.", style="bold bright_green")
                                # Move to new location
                                current_location = new_location
                                battle_found = True #!set flag
                            elif battle_outcome == "retreat":
                                console.print("You retreated from the battle", style="bold red")
                                battle_found = True #!set flag
                                break
                        else:
                            console.print("You already defeated this opponent", style = "green" )
                            current_location = new_location
                            battle_found = True #!set flag
                            break
                if not battle_found: #!changed from else
                    # No existing battle record

                    new_battle = Battle(player.id, opponent_at_location.id, 0)

                    # Add battle record to the database
                    new_battle.add_battle(player.id, opponent_at_location.id, 0)
                    # Start the battle


                    new_battle = Battle.get_battle_by_id(new_battle.id)#!new code added

                    battle_outcome = new_battle.start_battle(player, opponent_at_location, current_category)  # Pass current_category
                    # Check outcome of battle


                    if battle_outcome == "win":
                        console.print("You are ready for your next battle!", style="bold bright_green")
                        # Move to new location
                        current_location = new_location
                    elif battle_outcome == "retreat":
                        console.print("You retreated from the battle", style="bold red")
                        break
            else:
                # No opponent at the new location, move to new location

                click.echo("Continue exploring to find an opponent")
                click.echo()
                current_location = new_location

        elif current_location is None:
            print("Error: Invalid connected location ID.")
            break
        else:
            print("Error: Invalid direction. Please choose a valid direction.")

if __name__ == "__main__":
    welcome()
    main_menu()
