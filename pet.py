import random

MAX_STAT_VALUE = 100
MIN_STAT_VALUE = 0

class VirtualPet:
    def __init__(self, pet_type="cat"):
        """Initialize the pet with default values and an optional pet type."""
        self.pet_type = pet_type
        self.happiness = 50
        self.health = 50
        self.hunger = 50
        self.energy = 50
        self.level = 1
        self.experience = 0
        self.achievements = []

    def update_stat(self, stat, value, max_value=MAX_STAT_VALUE):
        """General method to update any stat with a boundary."""
        current_value = getattr(self, stat)
        new_value = min(max(current_value + value, MIN_STAT_VALUE), max_value)
        setattr(self, stat, new_value)

    def feed(self):
        """Feed the pet, improves hunger and happiness based on pet type."""
        if self.pet_type == "cat":
            self.update_stat("hunger", 15)
        elif self.pet_type == "dog":
            self.update_stat("hunger", 20)
        else:
            self.update_stat("hunger", 10)
        self.update_stat("happiness", 10)

    def play(self):
        """Play with the pet, increases happiness and energy."""
        self.update_stat("happiness", 20)
        self.update_stat("energy", -10)

    def study(self):
        """Increase pet's happiness, health, and energy based on study."""
        self.update_stat("happiness", 10)
        self.update_stat("health", 5)
        self.update_stat("energy", -15)
        self.gain_experience(10)

    def rest(self):
        """Rest to restore energy."""
        self.update_stat("energy", 20)
        self.update_stat("happiness", -5)

    def random_event(self):
        """Random events that affect the pet's state."""
        event = random.choice(["sick", "happy_event", "boredom", "new_favorite_activity"])
        
        if event == "sick":
            self.update_stat("health", -10)
            self.update_stat("happiness", -10)
            print("Your pet is feeling sick!")
        elif event == "happy_event":
            self.update_stat("happiness", 20)
            print("Your pet found something exciting!")
        elif event == "boredom":
            self.update_stat("happiness", -10)
            print("Your pet is feeling bored!")
        elif event == "new_favorite_activity":
            self.update_stat("happiness", 15)
            print("Your pet discovered a new favorite activity!")

    def gain_experience(self, amount):
        """Increase experience and level up if enough experience is gained."""
        self.experience += amount
        if self.experience >= 100:
            self.level_up()
            self.experience = 0

    def level_up(self):
        """Increase pet's level and improve some stats."""
        self.level += 1
        self.update_stat("happiness", 10)
        self.update_stat("energy", 10)

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


