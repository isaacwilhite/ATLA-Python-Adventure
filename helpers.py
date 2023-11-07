import click
from classes.player import *
import sys

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

##exit function
def check_quit(string):
    if string.lower() == "quit":
        click.echo("You have chosen to quit the game. What will we do without the Avatar! Please come back soon!")
    sys.exit()
