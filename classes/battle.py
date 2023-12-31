import sqlite3
import click
import random
from rich.console import Console
console = Console()
# Import Player class from the appropriate location

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Battle(): #!added status
    def __init__(self, player_id, opponent_id, status=0,id=None):
        self.player_id = player_id
        self.opponent_id = opponent_id
        self.status = status
        self.id = id


    def start_battle(self, player, opponent, category):
        #!comments out
        if self.status is None:
            self.status = 0  # Initialize status if it's None

        battle_result = self.battle(player, opponent, category)

        if battle_result == "win":
            console.print("You are one step closer to mastering all four elements!", style="bold bright_green")
            click.echo()
            console.print("Proceed to the next step to continue your journey in becoming the Avatar.", style="bold bright_green")
            click.echo()
            try:
                if self.status == 0:
                    self.update_battle_status(1)  # Update status if it's 0
                from classes.abilities import Abilities
                reward_list = [reward.strip() for reward in opponent.reward.split(',')]
                for reward in reward_list:

                    Abilities.create_db_instance(player.id, int(reward))
            except Exception as e:
                print(f"An error occurred while updating the database: {str(e)}")

            return "win"

        elif battle_result == "lose":
            player.faint()
            return "retreat"
        elif battle_result == "retreat":
            return "retreat"

    def battle(self, player, opponent, category):
        opponent_solution = [skill.strip() for skill in opponent.solution.split(',')]
        console.print(f"{opponent.name} says:", style="bold")
        click.echo()
        if category == "air":
            console.print(f"{opponent.dialogue}", style="#dc8c24")
            click.echo()
        elif category == "fire":
            console.print(f"{opponent.dialogue}", style="#890e05")
            click.echo()
        elif category == "water":
            console.print(f"{opponent.dialogue}", style="#66d7eb")
            click.echo()
        elif category == "earth":
            console.print(f"{opponent.dialogue}", style="#295427")
            click.echo()

        while opponent.health > 0 and player.health > 0:
            hint_skill = random.choice(opponent_solution)

            available_skills = player.get_all_skill_data_by_category(category)

            skill_info = next((skill for skill in available_skills if skill[0] == hint_skill), None)
            if skill_info is None:
                click.echo("You don't have any skills to use!")
                break

            skill_name, skill_description, skill_point_cost = skill_info

            hint_description = skill_info[1]
            click.echo(f"I think you may need {hint_description}.")
            click.echo()

            battle_result = self.perform_battle(available_skills, hint_skill)

            if battle_result == "win move":
                opponent.health -= skill_point_cost
                console.print(f"You've hit the opponent with {skill_name}!", style = "bold bright_green")
                click.echo()
                console.print(f"{opponent.name}'s health has decreased to: {opponent.health}", style="bold reverse red")

                opponent_solution.remove(hint_skill)
            elif battle_result == "lose move":
                player.decrease_health(1)
                console.print(f"The opponent has hit you! Your health is now {player.health}.", style="bold reverse red")
            elif battle_result == "retreat":
                click.echo("You've decided to retreat from battle.")
                return "retreat"

        if opponent.health <= 0:
            click.echo(f"Congratulations! You've defeated {opponent.name}!")
            return "win"
        elif player.health <= 0:
            click.echo(f"You've been defeated by {opponent.name}. Better luck next time!")
            return "lose"


    def perform_battle(self, available_skills, opponent_solution):
        for skill_info in available_skills:
            skill_name, skill_description, skill_point_cost = skill_info

        while True:
            skill_menu = {str(i + 1): skill[0] for i, skill in enumerate(available_skills)}
            skill_menu[str(len(available_skills) + 1)] = 'retreat'

            click.echo("Which move do you want to use?")
            click.echo()
            for i, skill_info in enumerate(available_skills):
                skill_name, _, _ = skill_info
                click.echo(f"{i + 1}. {skill_name}")

            skill_choice = click.prompt("Select a move", type=click.Choice(skill_menu.keys()))

            if skill_choice == str(len(available_skills) + 1):
                return "retreat"

            elif skill_choice.isdigit() and 1 <= int(skill_choice) <= len(available_skills):
                chosen_skill = available_skills[int(skill_choice) - 1][0]

                if chosen_skill == opponent_solution:
                    return "win move"
                else:
                    return "lose move"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS battles (
                id INTEGER PRIMARY KEY,
                player_id INTEGER,
                opponent_id INTEGER,
                status INTEGER,
                FOREIGN KEY (player_id) REFERENCES players(id) ON DELETE CASCADE,
                FOREIGN KEY (opponent_id) REFERENCES opponents(id)
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS battles
        """
        CURSOR.execute(sql)
        CONN.commit()

    def add_battle(self, player_id, opponent_id, status=0): #!remove status=0?
        sql = """
            INSERT INTO battles (player_id, opponent_id, status)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (player_id, opponent_id, status))
        CONN.commit()

        self.id = CURSOR.lastrowid

    def update_battle_status(self, status):
        sql = """
            UPDATE battles
            SET status = ?
            WHERE id = ?
        """
        try:
            CURSOR.execute(sql, (status, self.id))

            CONN.commit()

        except Exception as e:
            print(f"An error occurred while updating the database: {str(e)}")

    @classmethod
    def all_battles(cls):
        sql = """
            SELECT *
            FROM battles
        """
        rows = CURSOR.execute(sql).fetchall()

        return [cls(row[1], row[2], row[3], row[0]) for row in rows] #!adds row[3]

    @classmethod
    def get_battle_by_id(cls, id):
        sql = """
            SELECT *
            FROM battles
            WHERE id = ?
        """
        row = CURSOR.execute(sql, (id,)).fetchone()

        if row is not None:
            return cls(row[1], row[2], row[3], row[0]) #!adds row[3]
        return None

    @classmethod
    def all(cls):
        sql = """
            SELECT a.player_id, o.name
            FROM battles a
            JOIN opponents o ON a.opponent_id = o.id
            WHERE a.status = 1
        """
        CURSOR.execute(sql)
        records = CURSOR.fetchall()
        return [(record[0], record[1]) for record in records]
