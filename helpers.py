import click

def user_prompt():
    click.echo("Are you a returning user? (yes/no)")

    while True:
        user_choice = click.prompt("Your choice", type=click.Choice(['yes', 'no']))
        if user_choice in ['yes', 'no']:
            break
        else:
            click.echo("Invalid choice. Please enter 'yes' or 'no'.")

    if user_choice == 'yes':
        click.echo("Welcome back, young Avatar!")
    else:
        click.echo("Welcome, new Avatar!")

def helper_1():
    print("Performing useful function#1.")


def exit_program():
    print("Goodbye!")
    exit()
