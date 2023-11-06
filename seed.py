import sqlite3

from classes.player import Player
from classes.opponent import Opponent
from classes.nation import Nation
from classes.skill import Skill

#drop tables
Player.drop_table()
Opponent.drop_table()
Nation.drop_table()
Skill.drop_table()

#create tables
Player.create_table()
Opponent.create_table()
Nation.create_table()
Skill.create_table()

#table data
opponent_data = [
    ("Monk Tashi", "You have not been training hard enough! Let me test your skills in airbending and see if you can defeat me!", "air blast", 10, 1),
    ("Guru Pathik", "You must strengthen your spiritual connection to the world around you. Only by opening your chakras, can you finally master the Air element. Let’s test your skills!", "air blast, air scooter, air slice", 35, 2),
    ("Monk Giatso", "You have made it so far! I believe in your abilities to become an amazing Avatar. Let me see your bending in action before we give you your Airbending tattoos and make you a full airbender!", "air blast, air scooter, air slice, air glide, air shield", 70, 3)
]
nation_data = [
    ("Western Air Temple", "As you look around, you see the Air Temple lodged into the side of the cliff. The buildings seem to be upside-down and look like they are defying gravity. Here you can connect with the open skies and experience the freedom of Air bending.", "air"),
    ("Guru Pathik's Retreat", "Guru Pathik’s Retreat is an isolated and tranquil sanctuary where you will learn to strengthen your spiritual connection to Air bending. The high mountains will facilitate a deeper connection to the air and spirits around you.", "air"),
    ("Southern Air Temple", "You have reached the Southern Air Temple, birthplace of great Avatars that came before you! Can you feel the connection to all of your past selves! You will find mastery of the Air element here!", "air"),
    #potential edit appa's back
    ("Appa's Back", "You fainted! You wake up on Appa’s back restored and recharged.", "neutral" ),
    ("The Challenge Zone", "Here you will be faced with a challenge you must complete if you wish to advance.", "neutral" )
]

skill_data = [
    ("air blast", "powerful gust of wind that blasts opponents backwards", 10, "air"),
    ("air scooter", "ball of compressed air that allows the user to move away", 10, "air"),
    ("air shield", "protective barrier of air to block attacks", 10, "air"),
    ("air slice", "sharp blade used for cutting", 15, "air"),
    ("air swirl", "tornado-like vortex to disorient and attack opponents", 20, "air"),
    ("air glide", "glide through the air using bending", 15, "air")
]

# player_data = [
#     ("Tiana"),
#     ("Isaac"),
#     ("Michael")
# ]

#create instances

##opponent
for data in opponent_data:
    name, dialogue, solution, reward_id, nation_id = data
    Opponent.create(name, dialogue, solution, reward_id, nation_id)
##nation
for data in nation_data:
    name, description, category = data
    Nation.create(name, description, category)
##skill
for data in skill_data:
    name, description, point_cost, category = data
    Skill.create(name, description, point_cost, category)
##player data (more to see)
# for data in player_data:
#     username = data
#     Player.create(username)
