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
    ("Monk Tashi", "You have not been training hard enough! Let me test your skills in airbending and see if you can defeat me!", "Air Blast", 10, 2),
    ("Guru Pathik", "You must strengthen your spiritual connection to the world around you. Only by opening your chakras, can you finally master the Air element. Let’s test your skills!", "Air Blast,Air Scooter,Air Slice", 35, 3),
    ("Monk Giatso", "You have made it so far! I believe in your abilities to become an amazing Avatar. Let me see your bending in action before we give you your airbending tattoos and make you a full airbender!", "Air Blast,Air Scooter,Air Slice,Air Glide,Air Shield", 70, 4),
    ("King Bumi", "Young avatar you have much to learn. If you want to save your friends you must prove your skills are a match for mine!", "Rock Throw,Rock Cuffs,Rock Armor,Rock Gloves,Sand Blast", 70, 8),
    ("The Boulder", "You may be big, but you ain’t bad! The Boulder’s gonna win this, in a Land-slide!", "Rock Throw,Rock Cuffs,Rock Armor", 35, 9),
    ("Toph", "You have done well, but you need to kick it up a notch. Let’s work on form, you see, it comes from a strong stance.", "Rock Throw", 10, 10),
    ("Yue", "Use the moon to your advantage Avatar! As the moon increases your abilities, you will need to learn how to control them.", "Waterball,Ice Blade,Tidal Wave", 35, 12),
    ("Katara", "Okay, remember, I’m still learning too, so let’s take this nice and easy!", "Waterball", 10, 13),
    ("Due", "You’ve merely scratched the surface of your abilities, I've been learning for years. You're no match for me!", "Waterball,Ice Blade,Tidal Wave,Water Jet,Multiple Water Whips", 70, 14),
    ("Admiral Zhao", "I am Admiral Zhao, and my ambition burns brighter than the flames I command. Your little journey ends here, with your defeat!", "Blazing Arc", 10, 16),
    ("Prince Zuko", "I am Prince Zuko, son of Fire Lord Ozai, and I will regain my honor by defeating you!", "Blazing Arc,Ember Step,Inferno Pillar", 35, 17),
    ("Azula", "I’m Princess Azula. Only the best and strongest can stand by my side. Do you have what it takes, or will you crumble like so many before you?", "Blazing Arc,Ember Step,Inferno Pillar,Dragon's Maw,Phoenix Flight", 75, 18),
    ("Fire Lord Ozai", "I am Fire Lord Ozai, the Phoenix King, the most powerful firebender in the world. Bow before me or be consumed by my fire!", "Air Blast,Air Scooter,Air Slice,Air Glide,Air Shield,Rock Throw,Rock Cuffs,Rock Armor,Rock Gloves,Sand Blast,Waterball,Ice Blade,Tidal Wave,Water Jet,Multiple Water Whips,Blazing Arc,Ember Step,Inferno Pillar,Dragon's Maw,Phoenix Flight", 150, 19)
]

location_data = [
    ("Air Nomads", "Welcome to the Air Nomads! Here you can learn Air bending.", "air"),
    ("Western Air Temple", "As you look around, you see the Air Temple lodged into the side of the cliff. The buildings seem to be upside-down and look like they are defying gravity. Here you can connect with the open skies and experience the freedom of Air bending.", "air"),
    ("Guru Pathik's Retreat", "Guru Pathik’s Retreat is an isolated and tranquil sanctuary where you will learn to strengthen your spiritual connection to Air bending. The high mountains will facilitate a deeper connection to the air and spirits around you.", "air"),
    ("Southern Air Temple", "You have reached the Southern Air Temple, birthplace of great Avatars that came before you! Can you feel the connection to all of your past selves! You will find mastery of the Air element here!", "air"),
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
    ("Fire Nation Capital", "The skyline is dominated by the imposing silhouette of the royal palace greets you. The air is warm and the glow of flowing lava channels illuminates the streets.", "fire"),
    ("Ember Island", "You’re welcomed by the soft, warm sand beneath your feet and the soothing sound of gentle waves. The laid-back atmosphere contrasts sharply with the military precision of the mainland.", "fire"),
    ("The Boiling Rock", "A stark fortress amidst the mist of the boiling lake. The sheer heat is oppressive, and the impenetrable walls loom high.", "fire"),
    ("Final Battle", "Prepare to face your destiny with evil Fire Lord Ozai!", "neutral")
]

skill_data = [
    ("Air Blast", "powerful gust of wind that blasts opponents backwards", 10, "air"),
    ("Air Scooter", "ball of compressed air that allows the user to move away", 10, "air"),
    ("Air Shield", "protective barrier of air to block attacks", 20, "air"),
    ("Air Slice", "sharp blade used for cutting", 15, "air"),
    ("Air Swirl", "tornado-like vortex to disorient and attack opponents", 20, "air"),
    ("Air Glide", "glide through the air using bending", 15, "air"),
    ("Rock Throw", "Throw a large rock to damage opponents", 10, "earth"),
    ("Rock Cuffs", "Use the Earth to grab and immobilize your opponent", 15, "earth"),
    ("Rock Armor", "Create a layer of armor out of the earth", 20, "earth"),
    ("Sand Blast", "Generate a big blast of concentrated sand to weaken your opponent", 20, "earth"),
    ("Compressed Rock Bullets", "Turn rocks into bullets to pierce enemy armor", 25, "earth"),
    ("Rock Gloves", "Detachable hands, maintaining the hand shape able to grab and restrain the opponent from a distance.", 25, "earth"),
    ("Waterball", "Create a water ball to possibly use as defense or to slow opponents", 10, "water"),
    ("Ice Blade", "This Ice blade can be very sharp and might do some damage", 15, "water"),
    ("Water Jet", "Send a blast of water at your opponent", 15, "water"),
    ("Tidal Wave", "Creating a massive wave that can harm multiple opponents at once", 20, "water"),
    ("Multiple Water Whips", "These can be used to attack and defend from multiple angles at once", 25, "water"),
    ("Water Compression", "Having Enough power over water to compress its volume, compacting several thousands of gallons into a small volume", 25, "water"),
    ("Blazing Arc", "Creates a crescent-shaped wave of fire that sweeps across the battlefield, engulfing multiple enemies in flame.", 10, "fire"),
    ("Ember Step", "Firebender momentarily transforms into a flicker of flame, dashing to a new location. A burst of fire emanates outward, damaging nearby foes.", 15, "fire"),
    ("Inferno Pillar", "Summons a towering pillar of fire directly beneath the target erupting from the ground.", 20, "fire"),
    ("Dragon’s Maw", "Releases a concentrated, dragon-shaped burst of flame from their fists or mouth.", 20, "fire"),
    ("Cinder Shield", "Swirling vortex of flames around themselves, which serves as a defense mechanism. Incoming attacks are either incinerated or have their damage significantly reduced while this shield is active.", 15, "fire"),
    ("Phoenix Flight", "Ultimate display of fire mastery, this skill allows the firebender to launch into the air surrounded by a fiery aura, and then dive back down to the ground creating a massive explosion on impact.", 30, "fire")
]

player_data = [
    ("tiana"),
    ("isaac"),
    ("michael")
]

abilities_data = [
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4)
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
