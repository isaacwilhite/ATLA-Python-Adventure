import sqlite3

from classes.player import Player
from classes.opponent import Opponent
from classes.location import Location
from classes.skill import Skill
from classes.abilities import Abilities
from classes.battle import Battle

#drop tables
Player.drop_table()
Opponent.drop_table()
Location.drop_table()
Skill.drop_table()
Abilities.drop_table()
Battle.drop_table()

#create tables
Player.create_table()
Opponent.create_table()
Location.create_table()
Skill.create_table()
Abilities.create_table()
Battle.create_table()

#table data
opponent_data = [
    ("Monk Tashi", "You have not been training hard enough! Let me test your skills in airbending and see if you can defeat me!", "air blast", 10, 2),
    ("Guru Pathik", "You must strengthen your spiritual connection to the world around you. Only by opening your chakras, can you finally master the Air element. Let’s test your skills!", "air blast, air scooter, air slice", 35, 3),
    ("Monk Giatso", "You have made it so far! I believe in your abilities to become an amazing Avatar. Let me see your bending in action before we give you your Airbending tattoos and make you a full airbender!", "air blast, air scooter, air slice, air glide, air shield", 70, 4)
]
location_data = [
    ("Air Nomads", "Welcome to the Air Nomads! Here you can learn Air bending.", "air"),
    ("Western Air Temple", "As you look around, you see the Air Temple lodged into the side of the cliff. The buildings seem to be upside-down and look like they are defying gravity. Here you can connect with the open skies and experience the freedom of Air bending.", "air"),
    ("Guru Pathik's Retreat", "Guru Pathik’s Retreat is an isolated and tranquil sanctuary where you will learn to strengthen your spiritual connection to Air bending. The high mountains will facilitate a deeper connection to the air and spirits around you.", "air"),
    ("Southern Air Temple", "You have reached the Southern Air Temple, birthplace of great Avatars that came before you! Can you feel the connection to all of your past selves! You will find mastery of the Air element here!", "air"),
    #potential edit appa's back
    ("Appa's Back", "You fainted! You wake up on Appa’s back restored and recharged.", "neutral"),
    ("The Challenge Zone", "Here you will be faced with a challenge you must complete if you wish to advance.", "neutral"),
    ("Earth Kingdom", "Welcome to the Earth Kingdom! Here you can learn Earth bending.", "earth"),
    ("Omashu", "Omashu is a major Earth Kingdom City lead by King Bumi. Here you will learn that Earth bending isn’t all about strength and power. It’s more about learning when and how to strike.", "earth"),
    ("Chin Village", "You have entered Chin Village, a medium-sized town located on the cliffs of the Earth Kingdom's southwestern coast. It plays host to the Avatar Day festival. Learning to use your abilities to fight multiple opponents will aid you in your path.", "earth"),
    ("Ba Sing Se", "Welcome to Ba Sing Se, the capital of the Earth kingdom. Get ready to achieve mastery within the element of Earth, learning the last techniques needed to conquer this step in your journey.", "earth"),
    ("Water Tribe", "Welcome to the Water Tribe! Here you can learn Water bending.", "water"),
    ("Agna Qel’a", "The ice-fortress city is the capital of the North-pole. I’m guessing there’s some valuable information to be learned here.", "water"),
    ("South Pole", "There’s not much left, unfortunately the fire nation has destroyed most of what once stood. However, you may find some useful people here.", "water"),
    ("Foggy Swamp", "It’s a little dark, and these people are kind of strange. I know there’s a reason why we’re here. And… What's that smell?", "water"),
    ("Fire Nation", "Welcome to the Fire Nation! Here you can learn Fire bending.", "fire"),
    ("Fire Nation", "Welcome to the Fire Nation! Here you can learn Fire bending.", "fire"),
    ("Fire Nation", "Welcome to the Fire Nation! Here you can learn Fire bending.", "fire"),
    ("Fire Nation", "Welcome to the Fire Nation! Here you can learn Fire bending.", "fire")
]

skill_data = [
    ("air blast", "powerful gust of wind that blasts opponents backwards", 10, "air"),
    ("air scooter", "ball of compressed air that allows the user to move away", 10, "air"),
    ("air shield", "protective barrier of air to block attacks", 10, "air"),
    ("air slice", "sharp blade used for cutting", 15, "air"),
    ("air swirl", "tornado-like vortex to disorient and attack opponents", 20, "air"),
    ("air glide", "glide through the air using bending", 15, "air")
]

player_data = [
    ("tiana"),
    ("isaac"),
    ("michael")
]

abilities_data = [
    (1, 1),
    (1, 2),
    (1, 3)
]
#create instances

##opponent
for data in opponent_data:
    name, dialogue, solution, reward_id, location_id = data
    Opponent.create(name, dialogue, solution, reward_id, location_id)
##location
for data in location_data:
    name, description, category = data
    Location.create(name, description, category)
##skill
for data in skill_data:
    name, description, point_cost, category = data
    Skill.create(name, description, point_cost, category)
##player data (more to see)
for data in player_data:
    username = data
    Player.create_new_player(username)
##abilities
for data in abilities_data:
    player_id, skill_id = data
    Abilities.create_db_instance(player_id, skill_id)
