import simpy
import random

# Define the adventurers
class Adventurer:
    def __init__(self, name, luck, stealth, speed):
        self.name = name
        self.luck = luck
        self.stealth = stealth
        self.speed = speed
        self.alive = True # Each starts alive
        self.loots = {'diamonds': 0, 'rubies': 0, 'sapphires': 0, 'emeralds': 0, 'gold': 0} # Store the loot obtained from the lair in a dictionary
        self.successful_loots = 0

    def roll_dice(self):
        base_roll = random.randint(1, 20) # Roll 20 sided dice
        modifiers = self.luck + self.stealth + self.speed
        final_roll = base_roll if base_roll == 20 else base_roll + modifiers
        return base_roll, modifiers, final_roll # Final roll = dice roll + sum of each adventurer's modifiers

    def loot(self): # Randomize the loot obtained from each successful raid of the lair
        self.loots['diamonds'] += random.randint(5, 10)
        self.loots['rubies'] += random.randint(3, 7)
        self.loots['sapphires'] += random.randint(6, 8)
        self.loots['emeralds'] += random.randint(9, 14)
        self.loots['gold'] += random.randint(1,5)
        self.successful_loots += 1

# Stat modifiers for each adventurer
adventurers = [
    Adventurer('Sylas the Rogue', luck=0, stealth=3, speed=3),
    Adventurer('Lucian the Wizard', luck=3, stealth=1, speed=1),
    Adventurer('Belgrom the Dwarf', luck=1, stealth=1, speed=-2),
    Adventurer('Keldan the Elf', luck=2, stealth=2, speed=2)
]

# Define the Dragon's Lair environment
def dragon_lair(env, dragon_sleep, adventurers):
    while sum(adventurer.alive for adventurer in adventurers) > 1:
        print(f"Time {env.now}: The dragon is {'asleep' if dragon_sleep else 'awake'}")
        for adventurer in adventurers:
            if adventurer.alive: # Only living adventurers can try to steal from the lair
                base_roll, modifiers, final_roll = adventurer.roll_dice()
                print(f"{adventurer.name} rolls a {base_roll} + {modifiers} = {final_roll}")
                
                if final_roll >= 20:
                    print(f"{adventurer.name} successfully steals from the lair without breaking a sweat. The dragon slumbers.")
                    adventurer.loot()
                elif final_roll > 15:
                    print(f"{adventurer.name} successfully steals from the lair!")
                    adventurer.loot()
                elif final_roll > 10:
                    print(f"{adventurer.name} stumbles...")
                    if not dragon_sleep:
                        print(f"...the dragon wakes up. {adventurer.name} was scoured by flames.")
                        adventurer.alive = False
                    else:
                        print(f"{adventurer.name} made it out! The dragon slumbers.")
                        adventurer.loot()
                else:
                    print(f"{adventurer.name} was scoured by flames.")
                    adventurer.alive = False
        
        # Dragon sleeps for 14 hours per day
        dragon_sleep = not dragon_sleep
        sleep_duration = 14 if dragon_sleep else 10
        yield env.timeout(sleep_duration)
    
    # Check to see if all adventurers died
    if sum(adventurer.alive for adventurer in adventurers) == 0:
        print("\nOh no! The whole party was scoured by flames. No loot was obtained from the dragon's lair.")
    else:
        # If they did not all die, see who is the last one standing
        last_adventurer = None
        for adventurer in adventurers:
            if adventurer.alive:
                last_adventurer = adventurer

        if last_adventurer:
            # Print final loot screen
            loot = last_adventurer.loots
            print("\nFinal Results:")
            print(f"{last_adventurer.name} was the last one standing.")
            print(f"The final loot is {loot['diamonds']} diamonds, {loot['rubies']} rubies, {loot['sapphires']} sapphires, {loot['emeralds']} emeralds, and {loot['gold']} pounds of gold. Shiny!")
            print(f"{last_adventurer.name} looted from the dragon's lair {last_adventurer.successful_loots} times before calling it")
    for adventurer in adventurers:
        if not adventurer.alive:
            print(f"{adventurer.name} had {adventurer.successful_loots} successful loot(s) before dying.")

# Dragon starts asleep
dragon_sleep = True

# Initialize the SimPy environment
env = simpy.Environment()

# Run the dragon's lair and simulation
env.process(dragon_lair(env, dragon_sleep, adventurers))
env.run()
