import click
import sys
from classes.player import *

from helpers import exit_program

def welcome():
    file_path = 'txt/intro.txt'

    with open(file_path, 'r') as file:
        content = file.read()
        print(content)
##prompt user for a choice

def user_prompt():
    click.echo("Are you a returning user? (yes/no)")

    while True:
        user_choice = click.prompt("Your choice", type=click.Choice(['yes', 'no']))
        if user_choice == 'yes':
            return login_existing_user()
        elif user_choice == 'no':
            return create_new_user()
        elif user_choice == 'quit': #checks to see if player wants to quit
            check_quit()
        else:
            click.echo("Invalid choice. Please enter 'yes' or 'no'.")

def create_new_user():
    click.echo("Welcome, new Avatar! You can create your username now.")
    username = click.prompt("Please input your username:", type=str).lower().strip()
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

def login_existing_user(username):
    while True:
        username = click.prompt("Please input your username:", type=str).lower().strip()
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
    username = click.prompt("Please input your username to delete your player:", type=str).lower().strip()
    player = Player.find_by_username(username)

    while True:
        if player:
            confirm = click.prompt("Are you sure you want to delete your player? The four nations need your help! (yes/no)", type=click.Choice(['yes', 'no']))
            if confirm == 'yes':
                player.delete_player() #removes player from db and cascades removal of abilities
                click.echo("Player data deleted sucessfully")
            elif confirm == "no":
                click.echo("Player data was not deleted")
                #! type in menu to navigate back to the game (potential function)
            else:
                click.echo("Invalid choice. Please enter 'yes' or 'no'.")
        else:
            click.echo("Player not found. Please check your username.")

##exit function
def check_quit(string):
    if string.lower() == "quit":
        click.echo("You have chosen to quit the game. What will we do without the Avatar! Please come back soon!")
    sys.exit()

if __name__ == "__main__":
    welcome()
    user_prompt()
