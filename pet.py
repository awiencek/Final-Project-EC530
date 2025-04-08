import random
import sqlite3

import random

class VirtualPet:
    def __init__(self, pet_type="cat"):
        """Initialize the pet with default values and an optional pet type."""
        self.pet_type = pet_type  # Type of the pet (e.g., 'cat', 'dog')
        self.happiness = 50  # Pet's happiness on a scale from 0 to 100
        self.health = 50     # Pet's health on a scale from 0 to 100
        self.hunger = 50     # Pet's hunger on a scale from 0 to 100
        self.energy = 50     # Pet's energy on a scale from 0 to 100
        self.level = 1       # Level of pet (could be used for growth or upgrades)
        self.experience = 0  # Experience points for leveling up
        self.achievements = []  # List to store unlocked achievements

    def feed(self):
        """Feed the pet, improves hunger and happiness based on pet type."""
        if self.pet_type == "cat":
            self.hunger = min(self.hunger + 15, 100)
        elif self.pet_type == "dog":
            self.hunger = min(self.hunger + 20, 100)
        else:
            self.hunger = min(self.hunger + 10, 100)
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
        self.gain_experience(10)  # Gain experience from studying

    def rest(self):
        """Rest to restore energy."""
        self.energy = min(self.energy + 20, 100)
        self.happiness = max(self.happiness - 5, 0)

    def random_event(self):
        """Random events that affect the pet's state."""
        event = random.choice(["sick", "happy_event", "boredom", "new_favorite_activity"])
        
        if event == "sick":
            self.health = max(self.health - 10, 0)
            self.happiness = max(self.happiness - 10, 0)
            print("Your pet is feeling sick!")
        elif event == "happy_event":
            self.happiness = min(self.happiness + 20, 100)
            print("Your pet found something exciting!")
        elif event == "boredom":
            self.happiness = max(self.happiness - 10, 0)
            print("Your pet is feeling bored!")
        elif event == "new_favorite_activity":
            self.happiness = min(self.happiness + 15, 100)
            print("Your pet discovered a new favorite activity!")

    def gain_experience(self, amount):
        """Increase experience and level up if enough experience is gained."""
        self.experience += amount
        if self.experience >= 100:
            self.level_up()
            self.experience = 0  # Reset experience after leveling up
            print(f"{self.pet_type.capitalize()} leveled up!")

    def level_up(self):
        """Increase pet's level and improve some stats."""
        self.level += 1
        self.happiness = min(self.happiness + 10, 100)
        self.energy = min(self.energy + 10, 100)
        print(f"{self.pet_type.capitalize()} leveled up! Now at level {self.level}!")

    def get_status(self):
        """Returns the current status of the pet."""
        return {
            'happiness': self.happiness,
            'health': self.health,
            'hunger': self.hunger,
            'energy': self.energy,
            'level': self.level,
            'experience': self.experience
        }

    def is_sad(self):
        """Return True if the pet is unhappy, which could motivate the user to study more."""
        return self.happiness < 40

    def get_emotion(self):
        """Return a description of the pet's emotional state."""
        if self.happiness > 80:
            return "ecstatic"
        elif self.happiness > 60:
            return "happy"
        elif self.happiness > 40:
            return "content"
        elif self.happiness > 20:
            return "sad"
        else:
            return "depressed"

    def unlock_achievement(self, achievement_name):
        """Unlock a new achievement."""
        if achievement_name not in self.achievements:
            self.achievements.append(achievement_name)
            print(f"Achievement Unlocked: {achievement_name}")



class Database:
    def __init__(self):
        """Initialize the database connection."""
        self.conn = sqlite3.connect('study_buddy.db')
        self.cursor = self.conn.cursor()

    def create_table(self):
        """Create table to store pet state."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS pet_state (
                                happiness INTEGER,
                                health INTEGER,
                                hunger INTEGER,
                                energy INTEGER,
                                level INTEGER,
                                experience INTEGER)''')
        self.conn.commit()

    def save_pet_state(self, pet):
        """Save the pet's state to the database."""
        self.cursor.execute('''INSERT INTO pet_state (happiness, health, hunger, energy, level, experience)
                               VALUES (?, ?, ?, ?, ?, ?)''', 
                            (pet.happiness, pet.health, pet.hunger, pet.energy, pet.level, pet.experience))
        self.conn.commit()

    def load_pet_state(self):
        """Load the pet's state from the database."""
        self.cursor.execute('SELECT * FROM pet_state ORDER BY ROWID DESC LIMIT 1')
        row = self.cursor.fetchone()
        if row:
            pet = VirtualPet()
            pet.happiness, pet.health, pet.hunger, pet.energy, pet.level, pet.experience = row
            return pet
        return VirtualPet()  # Return a default pet if no state is found

    def close(self):
        """Close the database connection."""
        self.conn.close()

