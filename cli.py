import click

from helpers import (
    user_prompt,
    exit_program,
    helper_1
)

@click.command()
@click.option('--username', prompt='Enter your username', help='Your username to play the game')


def welcome():
    file_path = 'txt/intro.txt'

    with open(file_path, 'r') as file:
        content = file.read()
        print(content)
    ##prompt user for a choice

    user_prompt()


def main():
    while True:
        menu()
        choice = input("> ")
        if choice == "0":
            exit_program()
        elif choice == "1":
            helper_1()
        else:
            print("Invalid choice")


def menu():
    print("Please select an option:")
    print("0. Exit the program")
    print("1. Some useful function")


if __name__ == "__main__":
    welcome()
    main()
