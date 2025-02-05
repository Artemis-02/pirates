####################################################################################################
#IMPORTS
####################################################################################################

from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
import game.items as item
import random

#################################################################################################
#ISLAND DEFINITION
#################################################################################################

class Island(location.Location):

    def __init__(self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Island"
        self.symbol = "M"
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach(self)
        self.locations["fishing cove"] = Cove(self)
        self.locations["pirate hideout"] = PirateHideout(self)
        self.locations["temple"] = Temple(self)
        self.locations["dense forest"] = Forest(self)

        self.starting_location = self.locations["beach"]
    
    def enter(self, ship):
        display.announce("arrived at an island", pause=False)

class Beach(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs["south"] = self
        self.verbs["north"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.event_chance = 50
        self.events.append (seagull.Seagull())

    def enter(self):
        display.announce("Arrived at the beach. Your ship is at anchor in a small bay to th north\n"+
                         "Ahead of you is a dense forest that appears to cover the middle of this island completely\n"+
                         "The shore of this island appears to be safe enough to walk around the whole island on.")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "north"):
            display.announce("You return to your ship.")
            self.main_location.end_visit()
        elif (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["dense forest"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["fishing cove"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["pirate hideout"]

class Cove(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "fishing cove"
        self.verbs["south"] = self
        self.verbs["north"] = self
        self.verbs["west"] = self
        self.verbs["take"] = self
        self.verbs["fish"] = self

        self.item_on_the_shore = FishingSupplies()
        self.events.append(fishArtemis.FishingTrip())

    def enter(self):
        display.announce("As you walk around the shore of the island you come across a small cove.\n"+
                         "You see some fishing supplies and you see that the cove has a large population of fish.")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["temple"]

        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["beach"]

        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["dense forest"]

        elif (verb == "take"):
            item = self.item_on_the_shore
            config.the_player.add_to_inventory([item])
            display.announce("You pick up the fishing supplies, you believe they could be useful.")

        elif (verb == "fish"):
            self.event_chance = 100

#Temple + Riddles

class Temple(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "temple"
        self.verbs["north"] =self
        self.verbs["west"] = self
        self.verbs["east"] = self
        self.verbs["investigate"] = self
        self.item_in_temple = GoldenIdol()

    def enter(self):
        display.announce("As you walk around the shore of the island you come across an old temple.")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["dense forest"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["pirate hideout"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["fishing cove"]
        elif (verb == "investigate"):
            self.HandleTemple()
        
    def HandleTemple(self):
        if (not self.TempleUsed):
            display.announce("As you look around there isn't alot to see because most of the temple is falling apart.\n" +
                             "However one thing that catches your eye is a beautiful golden idol.\n" +
                             "As you go to grab it you the temple starts to shake and you hear a voice.\n" +
                             "If you wish to take from our temple you must prove your knowledge by answering our riddles.")
            choice = display.get_text_input("Do you wish to answer the riddles")
            if ("yes" in choice.lower()):
                self.HandleTempleRiddles()
            else:
                display.announce("You walk out of the temple", pause=False)
        else:
            display.announce("There nothing that catches your eye.", pause=False)
    
    def HandleTempleRiddles(self):
        riddles = self.GetRiddlesAndAnswerTemple()
        guesses = 3

        while guesses > 0:
            display.announce(riddles[0], pause=False)
            plural = ""
            if(guesses != 1):
                plural = "s"
            display.announce(f'You may guess {guesses} more time{plural}', pause=False)
            choice = display.get_text_input("What is your answer.")
            if riddles[1] == choice.lower():
                self.TempleReward()
                display.announce("Havng answered the tempe's spirts riddles you feel blessed and take the idol freely.")
                item = self.item_in_temple
                config.the_player.add_to_inventory([item])
                return
            else:
                guesses -= 1
                display.announce("Your answer is incorrect")
            if (guesses <= 0):
                self.TempleUsed = True
                display.announce("As you give your final incorrect answer you watch as the idol vanishes from your sight.")
                
        
    def GetRiddlesAndAnswerTemple(self):
        templeriddlelist = [["Cloaked in silence, I dance in the dark. I vanish by day, without leaving a mark. What am I?", "moon"],
                            ["At night they come without being fetched, and by day they are lost without being stolen", "stars"],
                            ["None can precieve without me, but all who look upon me lose their way.", "sun"]
                            ]
        return random.choice(templeriddlelist)
    
    def TempleReward(self):
        display.announce("Your answer is correct let your wounds be mended and may your travels under our beautiful night sky be blessed.")
        for c in config.the_player.get_pirates():
            c.lucky = True
            c.sick = False
            c.health = c.max_health
        self.TempleUsed = True

class PirateHideout(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "pirate hideout"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.events.append(PirateAttack())
        self.event_chance = 100
    
    def enter(self):
        display.announce("As you walk along the shore you come across what at first appears to be an abandoned village.\n" +
                         "However as you approach it you notice a few pirates jumping out of their hiding spots and they have you surrounded.")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["temple"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["dense forest"]

class Forest(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "dense forest"
        self.verbs["north"] = self
        self.verbs["south"] = self
        self.verbs["east"] = self
        self.verbs["west"] = self
        self.event_chance = 100
        self.events.append(MutatedApeCombat())
    
    def enter(self):
        display.announce("With diffuculties you start to walk through the small forest the cover the center of this island.\n" +
                         "After sometime you start to hear something that sounds like a animal.\n" +
                         "As you look around trying to find the sourse of that noice some sort of mutated monkey jumps down from a tree and starts attacking.")
    
    def process_verb(self, verb, cmd_list, nouns):
        if (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["beach"]
        elif (verb == "south"):
            config.the_player.next_loc = self.main_location.locations["temple"]
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["pirate hideout"]
        elif (verb == "east"):
            config.the_player.next_loc = self.main_location.locations["fishing cove"]

#################################################################################################
#ITEMS
#################################################################################################

class GoldenIdol(item.Item):
    def __init__(self):
        super().__init__("golden idol", 700)

class FishingSupplies(item.Item):
    def __init__(self):
        super().__init__("fishing supplies", 20)

#################################################################################################
#FIGHTS
#################################################################################################

class IslandPirates(combat.Monster):
    def __init__(self, name):
        attacks = {}
        attacks["punch"] = ["punches", random.randrange(35, 51), (1,10)] 
        attacks["stab"] = ["stabs", random.randrange(35,51), (1,10)]
        attacks["shot"] = ["shots", random.randrange(40,55), (5,15)]
        super().__init__("Ambush Pirate", random.randrange(5,15), attacks, 95 + random.randrange(-5,10))
        self.type_name = "Ambush Pirate"

class PirateAttack(event.Event):

    def __init__(self):
        self.name = "ambush pirate attack"
    
    def process(self, world):
        results = {}
        results["message"] = "The ambush pirates were defeated"
        attackers = []
        min = 3
        max = 5

        if random.randrange(2) == 0:
            min = 2
            max = 4
            attackers.append(IslandPirates("Ambush leader"))
            self.type_name = "Ambush leader"
            attackers[0].health = 2.2*attackers[0].health
        
        n_appearing = random.randrange(min, max)
        n = 1
        while n <= n_appearing:
            attackers.append(IslandPirates("Ambush pirate "+str(n)))
            n += 1
        display.announce("You are ambushed by a group of pirates!")
        combat.Combat(attackers).combat()
        results["newevents"] = [ self ]
        return results

class MutatedApe(combat.Monster):
    def __init__(self, name):
        attacks = {}
        attacks["punch"] = ["punches", random.randrange(60,80), (1,10)]
        attacks["bite"] = ["bites", random.randrange(45,50), (5,15)]#I want to add a sicking effect to this attack
        super().__init__("Mutated Ape", random.randrange(70,100), attacks, 70 + random.randrange(-10,0))
    
    #def resolve(self, action, moving, chosen_targets):

class MutatedApeCombat(event.Event):
    def __init__(self):
        self.name = "mutated ape attack"
    
    def process(self, world):
        results = {}
        ape = MutatedApe()
        display.announce("A mutated ape attacks your group.")
        combat.Combat([ape]).combat()
        display.announce("The mutated ape lays dead at your feet.")
        results["newevents"] = []
        results["message"] = ""
        return results
    
    #By Artemis Goheens