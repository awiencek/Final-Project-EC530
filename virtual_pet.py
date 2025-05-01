class Pet:
    def __init__(self, name="Buddy", level=1, experience=0, hunger=50, energy=50, happiness=50, streak=0, last_goal_completed_at=None):
        self.name = name
        self.level = level
        self.experience = experience
        self.hunger = hunger
        self.energy = energy
        self.happiness = happiness
        self.streak = streak
        self.last_goal_completed_at = last_goal_completed_at
        self.max_experience = 100 + (self.level - 1) * 20

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= self.max_experience:
            self.experience -= self.max_experience
            self.level += 1
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
        return (f"Name: {self.name}\n"
                f"Level: {self.level} (XP: {self.experience}/{self.max_experience})\n"
                f"Hunger: {self.hunger}/100  Energy: {self.energy}/100  Happiness: {self.happiness}/100\n"
                f"Streak: {self.streak} days")
