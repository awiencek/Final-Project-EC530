# pet.py
class Pet:
    def __init__(self, name="Buddy", level=1, experience=0, hunger=50, energy=50, happiness=50):
        """Initialize a new pet with given or default attributes."""
        self.name = name
        self.level = level
        self.experience = experience
        # Stats are on a 0–100 scale for simplicity:
        self.hunger = hunger       # 0 = not hungry (full), 100 = very hungry
        self.energy = energy       # 0 = exhausted, 100 = fully energized
        self.happiness = happiness # 0 = very sad, 100 = very happy
        # Experience needed for next level:
        self.max_experience = 100 + (self.level - 1) * 20

    def gain_experience(self, amount):
        """Increase experience points and handle level-ups if the threshold is reached."""
        self.experience += amount
        # Check for level up as long as we have enough XP for the next level
        while self.experience >= self.max_experience:
            self.experience -= self.max_experience
            self.level += 1
            # Recalculate next level's experience threshold
            self.max_experience = 100 + (self.level - 1) * 20

    def feed(self):
        """Feed the pet to satisfy hunger (reduces hunger level)."""
        # Decrease hunger (cannot go below 0). Also increase happiness slightly.
        self.hunger = max(self.hunger - 20, 0)
        self.happiness = min(self.happiness + 5, 100)

    def rest(self):
        """Let the pet rest to restore energy (and maybe increase hunger a bit)."""
        # Increase energy (up to 100). Hunger might increase slightly over rest.
        self.energy = min(self.energy + 30, 100)
        self.hunger = min(self.hunger + 5, 100)

    def play(self):
        """Play with the pet to boost happiness (uses some energy)."""
        # Increase happiness (up to 100). Decrease energy a bit due to activity.
        self.happiness = min(self.happiness + 20, 100)
        self.energy = max(self.energy - 10, 0)

    def study(self):
        """Study with the pet, increasing its experience (and consuming energy)."""
        # Studying yields experience and might tire the pet or make it hungry.
        self.gain_experience(15)            # gain some XP
        self.energy = max(self.energy - 10, 0)  # studying is tiring
        self.hunger = min(self.hunger + 10, 100) # and makes the pet a bit hungry

    def get_summary(self):
        """Return a formatted string summarizing the pet's status."""
        return (f"Name: {self.name}\n"
                f"Level: {self.level} (XP: {self.experience}/{self.max_experience})\n"
                f"Hunger: {self.hunger}/100  Energy: {self.energy}/100  Happiness: {self.happiness}/100")
