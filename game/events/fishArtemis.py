#Empty py intended as a suggestion for a type of event a student could add. 
# For ease of merging, students should append their names or other id to this py and any classes, to reduce conflicts.
from game import event
import random
import game.config as config
from game.items import Item
import game.display as display
from game import event

class FishingSupplies(Item):
    def __init__(self):
        super.__init__("fishing supplies", 20)

class FishingTrip(event.Event):
    def __init__(self):
        self.name = "you come across a good place to fish"
    def process(self, world):
        min = 4
        rng = random.randrange(1,10)
        fishes = random.randrange(1,5)
        num = 1
        c =random.choice(config.the_player.get_pirates())
        s = False
        l = False
        for i in config.the_player.inventory:
            if type(i) == FishingSupplies:
                min += 2
                s = True
        if c.Lucky():
            min += 2
            l = True
        if min >= rng:
            if num < fishes:
                caught = num
            else:
                caught = fishes
        plural = ""
        if caught != 0:
            plural = "es"
        if ((s and l) == True):
            display.announce(f"Using your fishing supplies and a bit of luck you caught {caught} fish{plural}.")
        elif s ==True:
            display.announce(f"Using your fishing supplies you caught {caught} fish{plural}.")
        elif l == True:
            display.announce(f"With some luck you caught {caught} fish{plural}.")
        elif ((s and l) == False):
            display.announce(f"You were able to catch {caught} fish{plural}.")
        config.the_player.ship.food += caught
