import sqlite3
import click
import random

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Battle():
    def __init__(self, player_id, opponent_id, status=0, id=None):
        self.player_id = player_id
        self.opponent_id = opponent_id
        self.status = status
        self.id = id

#!must add properties to the different attributes

    def start_battle(self, player, opponent, category):
        battle_result = self.battle(player, opponent, category)

        if battle_result == "win":
            click.echo("Congratulations! You are one step closer to mastering all four elements! Proceed to the next step to continue your journey in becoming the Avatar.")
            try:
                self.update_battle_status(1)
                from abilities import Abilities
                # Abilities.create_db_instance(player.id, place_holder)
                #~add new skill to Abilities Class (existing function)
                #! think about how to dynamically change the skill_id you want to add
            except Exception as e:
                print(f"An error occurred while updating the database: {str(e)}")

            return "win"

        elif battle_result == "lose":
            try:
                self.update_battle_status(0)
            except Exception as e:
                print(f"An error occurred while updating the database: {str(e)}")

            from player import Player
            player.faint()
            return "retreat"
        elif battle_result == "retreat":
            return "retreat"

    def battle(self, player, opponent, category):
        opponent_solution = [skill.strip() for skill in opponent.solution.split(',')]
        click.echo(opponent.dialogue)

        while opponent.health > 0 and player.health > 0:
            hint_skill = random.choice(opponent_solution)

            available_skills = player.get_all_skill_data_by_category(category)
            skill_info = next((skill for skill in available_skills if skill[0] == hint_skill), None)

            if skill_info is None:
                click.echo("You don't have any skills to use!")
                break

            skill_name, skill_description, skill_point_cost = skill_info

            hint_description = skill_info[1]  # Description of the matching skill
            click.echo(f"I think you may need something that will {hint_description}.")

            battle_result = self.perform_battle(available_skills, hint_skill)

            if battle_result == "win move":
                opponent.health -= skill_point_cost
                click.echo(f"You've hit the opponent with {skill_name}!")
                opponent_solution.remove(hint_skill)
            elif battle_result == "lose move":
                player.decrease_health(1)
                click.echo(f"The opponent has hit you! Your health is now {player.health}.")
            elif battle_result == "retreat":
                click.echo("You've decided to retreat from battle.")
                return "retreat"

        if opponent.health <= 0:
            click.echo(f"Congratulations! You've defeated {opponent.name}!")
            return "win"
        elif player.health <= 0:
            click.echo(f"You've been defeated by {opponent.name}. Better luck next time!")
            return "lose"

    def get_player_skill_choice(self, available_skills):
        skill_menu = {str(i + 1): skill for i, skill in enumerate(available_skills)}
        click.echo("Choose a skill to use:")
        return click.prompt(menu=skill_menu, type=click.Choice(skill_menu.keys()))

    #~ handles every move that a player makes
    def perform_battle(self, available_skills, opponent_solution):
        while True:
            skill_menu = {str(i + 1): skill[0] for i, skill in enumerate(available_skills)}
            skill_menu[str(len(available_skills) + 1)] = 'retreat'

            click.echo("Which move do you want to use?")
            for i, skill_name in enumerate(available_skills):
                click.echo(f"{i + 1}. {skill_name}")

            skill_choice = click.prompt("Select a move", type=click.Choice(skill_menu.keys()))

            if skill_choice == str(len(available_skills) + 1):
                return "retreat"

            elif skill_choice.isdigit() and 1 <= int(skill_choice) <= len(available_skills):
                chosen_skill = available_skills[int(skill_choice) - 1]
                if chosen_skill == opponent_solution:
                    return "win move"
                else:
                    return "lose move"
            else:
                click.echo("Invalid input. Please select an appropriate choice.")
#!automatic checkpoint function
    #~~~~~~~~~~~~~~~~~~~~~~CRUD~~~~~~~~~~~~~~~~~~~
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

    def add_battle(self, player_id, opponent_id, status):
        sql = """
            INSERT INTO battles (player_id, opponent_id, status)
            VALUES (?, ?, ?)
        """
        CURSOR.execute(sql, (player_id, opponent_id, status))
        CONN.commit()

    def update_battle_status(self, status):
        sql = """
            UPDATE battles
            SET status = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (status, self.id))
        CONN.commit()

#!returns list of all battle instances
    @classmethod
    def all_battles(cls):
        sql = """
            SELECT *
            FROM battles
        """
        rows = CURSOR.execute(sql).fetchall()
        return [cls(*row) for row in rows]
#!returns battle by battle id
    @classmethod
    def get_battle_by_id(cls, id):
        sql = """
            SELECT *
            FROM battles
            WHERE id = ?
        """
        battle_instance = CURSOR.execute(sql, (id,)).fetchone()
        if battle_instance is not None:
            return cls(*battle_instance)
        return None

#association method
    #battles that were won
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
