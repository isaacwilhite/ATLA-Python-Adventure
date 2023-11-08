import sqlite3
import click
import random

CONN = sqlite3.connect("database.db")
CURSOR = CONN.cursor()

class Battle():
    def __init__(self, player_id, opponent_id, challenge_id, status, id=None):
        self.player_id = player_id
        self.opponent_id = opponent_id
        self.challenge_id = challenge_id
        self.status = status
        self.id = id
#!if the status is 0 then just have a value
    def start_battle(self, player, map_location):
        #what opponents are available at that location
        available_opponents = self.available_opponents(map_location, player)

        #!Battle Loop
        #no loop needed, only put in one opponent
        for opponent in available_opponents:
            battle_result = self.battle(player, opponent)

            if battle_result == "win":
                click.echo("Congratulations! You are one step closer to mastering all four elements! Proceed to the next step to continue your journey in becoming the Avatar.")
                try:
                    self.update_battle_status(1)
                    from abilities import Abilities
                    # Abilities.create_db_instance(player.id, place_holder)
                    #~add new skill to Abilities Class (existing function)
                    #! think about how to dynamically change the skill_id you want to add
                except:
                    raise Exception("Unable to update database")

            elif battle_result == "lose":
                from player import Player
                player.faint()
                #!reset location
            elif battle_result == "retreat":
                break
                #! use function that reset_map() takes you back to the beginning

    def available_opponents(self, map_location, player):
        #! pass in a map_location and player progress (which battles are lost (0))
        #!return list of available opponents
        pass

    def battle(self, player, opponent, category):
        opponent_solution = [skill.strip() for skill in opponent.solution.split(',')]
        click.echo(opponent.dialogue)

        while opponent.health > 0 and player.health > 0:
            hint_skill = random.choice(opponent_solution)

            from player import Player
            available_skills = player.get_all_skill_data_by_category(category)
            skill_info = next((skill for skill in available_skills if skill[0] == hint_skill), None)

            if skill_info is None:
                click.echo("You don't have any skills to use!")
                break

            skill_name, skill_description, skill_point_cost = skill_info
            skill_choice = skill_name  # The player directly uses the skill

            hint_description = skill_info[1]  # Description of the matching skill
            click.echo(f"I think you may need something that will {hint_description}.")

            battle_result = self.perform_battle(available_skills, hint_skill)

            if battle_result == "win":
                opponent.health -= skill_point_cost
                click.echo(f"You've hit the opponent with {skill_name}!")
                opponent_solution.remove(hint_skill)
            elif battle_result == "lose":
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
                    return "win"
                else:
                    return "lose"
            else:
                click.echo("Invalid input. Please select an appropriate choice.")
#!automatic checkpoint function
#!checkpoint in map menu#!split on ", " and if this in player.skills
#!iterate aovera all of the abilities they have
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

#association method
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
