# study_buddy.py
import tkinter as tk
from tkinter import simpledialog, messagebox
from pet import VirtualPet
from database import Database

class StudyBuddyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Virtual Study Buddy")

        # Initialize the pet and database
        self.pet = VirtualPet()
        self.db = Database()

        # Fetch pet status from the database or use default
        pet_status = self.db.get_pet_status()
        if pet_status:
            self.pet.happiness = pet_status['happiness']
            self.pet.health = pet_status['health']
            self.pet.hunger = pet_status['hunger']
            self.pet.energy = pet_status['energy']
            self.pet.level = pet_status['level']

        # Create UI elements
        self.create_widgets()

    def create_widgets(self):
        """Set up the GUI widgets."""
        self.status_label = tk.Label(self.root, text="Pet Status")
        self.status_label.pack()

        self.happiness_label = tk.Label(self.root, text=f"Happiness: {self.pet.happiness}")
        self.happiness_label.pack()

        self.energy_label = tk.Label(self.root, text=f"Energy: {self.pet.energy}")
        self.energy_label.pack()

        self.study_button = tk.Button(self.root, text="Study", command=self.study)
        self.study_button.pack()

        self.feed_button = tk.Button(self.root, text="Feed Pet", command=self.feed_pet)
        self.feed_button.pack()

        self.play_button = tk.Button(self.root, text="Play with Pet", command=self.play_with_pet)
        self.play_button.pack()

        self.goal_button = tk.Button(self.root, text="Set Study Goal", command=self.set_study_goal)
        self.goal_button.pack()

    def update_pet_status(self):
        """Update the pet's status in the GUI."""
        self.happiness_label.config(text=f"Happiness: {self.pet.happiness}")
        self.energy_label.config(text=f"Energy: {self.pet.energy}")

    def study(self):
        """Simulate studying."""
        self.pet.study()
        self.update_pet_status()
        self.db.save_pet_status(self.pet)
        messagebox.showinfo("Study Complete", "You studied hard! Your pet is happier!")

    def feed_pet(self):
        """Feed the pet."""
        self.pet.feed()
        self.update_pet_status()
        self.db.save_pet_status(self.pet)
        messagebox.showinfo("Pet Fed", "Your pet is full and happy!")

    def play_with_pet(self):
        """Play with the pet."""
        self.pet.play()
        self.update_pet_status()
        self.db.save_pet_status(self.pet)
        messagebox.showinfo("Play Time", "Your pet had fun playing!")

    def set_study_goal(self):
        """Set a new study goal."""
        goal = simpledialog.askstring("New Goal", "What is your study goal?")
        if goal:
            self.db.add_study_goal(goal)
            messagebox.showinfo("Goal Set", f"Your new study goal: {goal}")
    
# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = StudyBuddyApp(root)
    root.mainloop()
