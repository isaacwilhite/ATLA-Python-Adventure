import click
import sys

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
            login_existing_user()
        elif user_choice == 'no':
            create_new_user()
        elif user_choice == 'quit': #checks to see if player wants to quit
            check_quit()
        else:
            click.echo("Invalid choice. Please enter 'yes' or 'no'.")

def create_new_user():
    # Implement the logic to create a new user
    # You can prompt for additional user information if needed
    click.echo("Welcome, new Avatar! You can create your character now.")
    # Add code to handle user registration

def login_existing_user(username):
    username = click.prompt("Please input your username:", type=str).lower().strip()
    #check if they wanna quit
    check_quit(username)



    # Implement the logic to log in an existing user
    # You can prompt for the user's password or other login details
    click.echo(f"Welcome back, {username}! You can resume your journey as an Avatar.")
    # Add code to handle user login

##exit function
def check_quit(string):
    if string.lower() == "quit":
        click.echo("You have chosen to quit the game. What will we do without the Avatar! Please come back soon!")
    sys.exit()

if __name__ == "__main__":
    welcome()
    user_prompt()
    exit_program
