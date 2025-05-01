
import tkinter as tk
from pet import Pet
from database import StudyAppDB

# Initialize the database and pet
db = StudyAppDB()
pet_data = db.load_pet("Buddy")
if pet_data:
    pet = Pet(**pet_data)
else:
    pet = Pet(name="Buddy")
    db.save_pet_state(pet)

# Setup the main application window
root = tk.Tk()
root.title("Virtual Study Pet")
root.geometry("300x270")  # slightly taller to fit streak label
root.resizable(False, False)

# Placeholder canvas for future pet image or background
canvas = tk.Canvas(root, width=100, height=100, bg="lightgray")
canvas.pack(pady=5)

# Label to display pet status
status_var = tk.StringVar()
status_var.set(pet.get_summary())
status_label = tk.Label(root, textvariable=status_var, justify=tk.LEFT)
status_label.pack(pady=5)

# Label to display current streak
treak_var = tk.StringVar()
streak_var.set(f"Streak: {pet.streak} days")
streak_label = tk.Label(root, textvariable=streak_var)
streak_label.pack(pady=2)

# Define button actions to interact with the pet
def handle_study():
    pet.study()
    db.save_pet_state(pet)
    status_var.set(pet.get_summary())
    streak_var.set(f"Streak: {pet.streak} days")

def handle_feed():
    pet.feed()
    db.save_pet_state(pet)
    status_var.set(pet.get_summary())
    streak_var.set(f"Streak: {pet.streak} days")

def handle_rest():
    pet.rest()
    db.save_pet_state(pet)
    status_var.set(pet.get_summary())
    streak_var.set(f"Streak: {pet.streak} days")

def handle_play():
    pet.play()
    db.save_pet_state(pet)
    status_var.set(pet.get_summary())
    streak_var.set(f"Streak: {pet.streak} days")

# Action buttons frame
button_frame = tk.Frame(root)
button_frame.pack(pady=5)
tk.Button(button_frame, text="Study", command=handle_study, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Feed", command=handle_feed, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Rest", command=handle_rest, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Play", command=handle_play, width=8).pack(side=tk.LEFT, padx=5)

# Cleanup: close the database when the window is closed
def on_close():
    db.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# Start the Tkinter event loop
root.mainloop()
