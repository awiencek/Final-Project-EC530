from datetime import datetime, timedelta

class Pet:
    def __init__(self, name="Buddy", level=1, experience=0, hunger=50, energy=50,
                 happiness=50, streak=0, last_goal_completed_at=None, last_decay_check=None,
                 paused=False, subject="General"):
        self.name = name
        self.level = level
        self.experience = experience
        self.hunger = hunger
        self.energy = energy
        self.happiness = happiness
        self.streak = streak
        self.last_goal_completed_at = last_goal_completed_at
        self.last_decay_check = last_decay_check or datetime.now().isoformat()
        self.paused = paused
        self.subject = subject
        self.max_experience = 100 + (self.level - 1) * 20

    def gain_experience(self, amount):
        self.experience += amount
        while self.experience >= self.max_experience:
            self.experience -= self.max_experience
            self.level += 1
            self.max_experience = 100 + (self.level - 1) * 20

    def feed(self):
        self.hunger = max(self.hunger - 20, 0)
        self.happiness = min(self.happiness + 5, 100)

    def rest(self):
        self.energy = min(self.energy + 30, 100)
        self.hunger = min(self.hunger + 5, 100)

    def play(self):
        self.happiness = min(self.happiness + 20, 100)
        self.energy = max(self.energy - 10, 0)

    def study(self):
        self.gain_experience(15)
        self.energy = max(self.energy - 10, 0)
        self.hunger = min(self.hunger + 10, 100)

    def get_summary(self):
        return (f"Name: {self.name}\n"
                f"Subject: {self.subject}\n"
                f"Level: {self.level} (XP: {self.experience}/{self.max_experience})\n"
                f"Hunger: {self.hunger}/100  Energy: {self.energy}/100  Happiness: {self.happiness}/100\n"
                f"Streak: {self.streak} days")

    def toggle_pause(self):
        self.paused = not self.paused

    def apply_decay(self):
        if self.paused:
            return

        now = datetime.now()
        try:
            last_checked = datetime.fromisoformat(self.last_decay_check)
        except Exception:
            last_checked = now

        hours_passed = (now - last_checked).total_seconds() / 3600
        if hours_passed < 1:
            return

        decay_hours = int(hours_passed)
        self.hunger = min(self.hunger + 5 * decay_hours, 100)
        self.energy = max(self.energy - 3 * decay_hours, 0)
        self.happiness = max(self.happiness - 2 * decay_hours, 0)

        self.last_decay_check = now.isoformat()
