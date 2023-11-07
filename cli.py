import click
import sys
from classes.player import *
from classes.abilities import *
from helpers import (
    create_new_user,
    login_existing_user,
    remove_player_from_db,
    check_quit
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
        click.echo("2. Start Game")
        click.echo("1. Check Skills")
        click.echo("2. Check Health")
        click.echo("3. Quit Adventure")

        adventure_choice = click.prompt("Choose an option (1/2/3)", type=click.Choice(['1', '2', '3']))

        if adventure_choice == '1':
            pass
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


if __name__ == "__main__":
    welcome()
    main_menu()
