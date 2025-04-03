# pet.py
import random

class VirtualPet:
    def __init__(self):
        self.happiness = 50  # Pet's happiness on a scale from 0 to 100
        self.health = 50     # Pet's health on a scale from 0 to 100
        self.hunger = 50     # Pet's hunger on a scale from 0 to 100
        self.energy = 50     # Pet's energy on a scale from 0 to 100
        self.level = 1       # Level of pet (could be used for growth or upgrades)

    def feed(self):
        """Feed the pet, improves hunger and happiness."""
        self.hunger = min(self.hunger + 20, 100)
        self.happiness = min(self.happiness + 10, 100)

    def play(self):
        """Play with the pet, increases happiness and energy."""
        self.happiness = min(self.happiness + 20, 100)
        self.energy = max(self.energy - 10, 0)

    def study(self):
        """Increase pet's happiness, health, and energy based on study."""
        self.happiness = min(self.happiness + 10, 100)
        self.health = min(self.health + 5, 100)
        self.energy = max(self.energy - 15, 0)

    def rest(self):
        """Rest to restore energy."""
        self.energy = min(self.energy + 20, 100)
        self.happiness = max(self.happiness - 5, 0)

    def get_status(self):
        """Returns the current status of the pet."""
        return {
            'happiness': self.happiness,
            'health': self.health,
            'hunger': self.hunger,
            'energy': self.energy,
            'level': self.level
        }

    def level_up(self):
        """Increase pet's level, could unlock new features or change appearance."""
        self.level += 1
        self.happiness = min(self.happiness + 10, 100)
        self.energy = min(self.energy + 10, 100)

    def is_sad(self):
        """Return True if the pet is unhappy, which could motivate the user to study more."""
        return self.happiness < 40

