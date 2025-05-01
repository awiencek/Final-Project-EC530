import tkinter as tk
from pet import Pet
from database import StudyAppDB
from datetime import datetime

# Initialize the database and pet
db = StudyAppDB()
pet_data = db.load_pet("Buddy")
if pet_data:
    pet = Pet(**pet_data)
else:
    pet = Pet(name="Buddy")
    db.save_pet_state(pet)

# Apply any needed stat decay on load
pet.apply_decay()
db.save_pet_state(pet)

# Setup the main application window
root = tk.Tk()
root.title("Virtual Study Pet")
root.geometry("300x310")  # taller to fit toggle button
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
streak_var = tk.StringVar()
streak_var.set(f"Streak: {pet.streak} days")
streak_label = tk.Label(root, textvariable=streak_var)
streak_label.pack(pady=2)

# Label to show decay status
decay_status_var = tk.StringVar()
decay_status_var.set("Decay: Active" if not pet.paused else "Decay: Paused")
decay_label = tk.Label(root, textvariable=decay_status_var)
decay_label.pack(pady=2)

# Define button actions to interact with the pet
def refresh_ui():
    status_var.set(pet.get_summary())
    streak_var.set(f"Streak: {pet.streak} days")
    decay_status_var.set("Decay: Active" if not pet.paused else "Decay: Paused")

def handle_study():
    pet.study()
    db.save_pet_state(pet)
    refresh_ui()

def handle_feed():
    pet.feed()
    db.save_pet_state(pet)
    refresh_ui()

def handle_rest():
    pet.rest()
    db.save_pet_state(pet)
    refresh_ui()

def handle_play():
    pet.play()
    db.save_pet_state(pet)
    refresh_ui()

def toggle_decay():
    pet.toggle_pause()
    db.save_pet_state(pet)
    refresh_ui()

# Action buttons frame
button_frame = tk.Frame(root)
button_frame.pack(pady=5)
tk.Button(button_frame, text="Study", command=handle_study, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Feed", command=handle_feed, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Rest", command=handle_rest, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Play", command=handle_play, width=8).pack(side=tk.LEFT, padx=5)

# Pause decay toggle button
tk.Button(root, text="Toggle Nap/Vacation", command=toggle_decay).pack(pady=5)

# Cleanup: close the database when the window is closed
def on_close():
    db.save_pet_state(pet)
    db.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# Start the Tkinter event loop
root.mainloop()


root.protocol("WM_DELETE_WINDOW", on_close)

# Start the Tkinter event loop
root.mainloop()
