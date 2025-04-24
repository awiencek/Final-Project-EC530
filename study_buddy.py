import tkinter as tk
from tkinter import simpledialog, messagebox
from virtual_pet import VirtualPet
from pet_database import PetDatabase
from study_goal_database import StudyGoalDatabase

class StudyBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Study Buddy")

        # Initialize the pet and database
        self.pet = VirtualPet()
        self.pet_db = PetDatabase()
        self.study_goal_db = StudyGoalDatabase()

        # Fetch pet status from the database or use default
        self.pet = self.pet_db.load_pet_state()

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        """Set up the GUI widgets."""
        self.status_label = tk.Label(self.root, text="Pet Status")
        self.status_label.pack()

        # Happiness, energy, and emotional state labels
        self.happiness_label = tk.Label(self.root, text=f"Happiness: {self.pet.happiness}")
        self.happiness_label.pack()

        self.energy_label = tk.Label(self.root, text=f"Energy: {self.pet.energy}")
        self.energy_label.pack()

        self.level_label = tk.Label(self.root, text=f"Level: {self.pet.level}")
        self.level_label.pack()

        self.experience_label = tk.Label(self.root, text=f"Experience: {self.pet.experience}")
        self.experience_label.pack()

        self.emotion_label = tk.Label(self.root, text=f"Emotion: {self.pet.get_emotion()}")
        self.emotion_label.pack()

        # Buttons for interacting with the pet
        self.study_button = tk.Button(self.root, text="Study", command=self.study)
        self.study_button.pack()

        self.feed_button = tk.Button(self.root, text="Feed Pet", command=self.feed_pet)
        self.feed_button.pack()

        self.play_button = tk.Button(self.root, text="Play with Pet", command=self.play_with_pet)
        self.play_button.pack()

        self.rest_button = tk.Button(self.root, text="Rest Pet", command=self.rest_pet)
        self.rest_button.pack()

        self.random_event_button = tk.Button(self.root, text="Random Event", command=self.random_event)
        self.random_event_button.pack()

        self.goal_button = tk.Button(self.root, text="Set Study Goal", command=self.set_study_goal)
        self.goal_button.pack()

        # Button for unlocking achievements
        self.achievement_button = tk.Button(self.root, text="Unlock Achievement", command=self.unlock_achievement)
        self.achievement_button.pack()

    def update_pet_status(self):
        """Update the pet's status in the GUI."""
        self.happiness_label.config(text=f"Happiness: {self.pet.happiness}")
        self.energy_label.config(text=f"Energy: {self.pet.energy}")
        self.level_label.config(text=f"Level: {self.pet.level}")
        self.experience_label.config(text=f"Experience: {self.pet.experience}")
        self.emotion_label.config(text=f"Emotion: {self.pet.get_emotion()}")

    def study(self):
        """Simulate studying."""
        self.pet.study()
        self.update_pet_status()
        self.pet_db.save_pet_state(self.pet)
        messagebox.showinfo("Study Complete", "You studied hard! Your pet is happier!")

    def feed_pet(self):
        """Feed the pet."""
        self.pet.feed()
        self.update_pet_status()
        self.pet_db.save_pet_state(self.pet)
        messagebox.showinfo("Pet Fed", "Your pet is full and happy!")

    def play_with_pet(self):
        """Play with the pet."""
        self.pet.play()
        self.update_pet_status()
        self.pet_db.save_pet_state(self.pet)
        messagebox.showinfo("Play Time", "Your pet had fun playing!")

    def rest_pet(self):
        """Rest to restore energy."""
        self.pet.rest()
        self.update_pet_status()
        self.pet_db.save_pet_state(self.pet)
        messagebox.showinfo("Rest Time", "Your pet is resting and regaining energy.")

    def random_event(self):
        """Trigger a random event for the pet."""
        self.pet.random_event()
        self.update_pet_status()
        self.pet_db.save_pet_state(self.pet)

    def unlock_achievement(self):
        """Unlock an achievement."""
        achievement_name = simpledialog.askstring("Unlock Achievement", "Enter achievement name:")
        if achievement_name:
            self.pet.unlock_achievement(achievement_name)
            messagebox.showinfo("Achievement Unlocked", f"Achievement unlocked: {achievement_name}")
    
    def set_study_goal(self):
        """Set a new study goal."""
        goal = simpledialog.askstring("New Goal", "What is your study goal?")
        if goal


