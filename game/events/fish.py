#Empty py intended as a suggestion for a type of event a student could add. 
# For ease of merging, students should append their names or other id to this py and any classes, to reduce conflicts.
from game import event
import random
import game.config as config

#class FishingTrip(event.Event):
'''min = 4
rng = random.randint(1,10)
fishes = random.randint(1, 5)
num = 1
c = random.choice(config.the_player.get_pirates())
s = False
l = False
if "fishing supplies" in config.the_player.inventory([item]):
    min = min + 2
    num += 2
    s = True
elif c.isLucky() == True:
    min = min + 2
    num +=2
    l = True
if min >= rng:
    if num < fishes:
        caught = num
    else:
        caught = fishes
plural = ""
if caught != 1:
    plural = "es"
if ((s and l) == True):
    display.announce(f"Using your fishing supplies and a bit of luck you caught {caught} fish{plural}.")
elif s ==True:
    display.announce(f"Using your fishing supplies you caught {caught} fish{plural}.")
elif l == True:
    display.announce(f"With some luck you caught {caught} fish{plural}.")
elif ((s and l) == False):
    display.announce(f"You were able to catch {caught} fish{plural}.")
config.the_player.ship.food += caught'''