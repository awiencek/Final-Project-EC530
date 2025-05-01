import tkinter as tk
from tkinter import simpledialog, messagebox
from pet import Pet
from database import StudyAppDB
from datetime import datetime

# Initialize DB and fetch pet list
db = StudyAppDB()
pets = db.list_pets()
pet_names = [name for name, _ in pets]

# Prompt user to choose or create a pet
root = tk.Tk()
root.withdraw()

if pet_names:
    selected_name = simpledialog.askstring("Select Pet", f"Available pets: {', '.join(pet_names)}\nEnter pet name to load, or leave blank to create a new one:")
else:
    selected_name = None

if selected_name and selected_name in pet_names:
    pet_data = db.load_pet(selected_name)
    pet = Pet(**pet_data)
else:
    new_name = simpledialog.askstring("New Pet", "Enter new pet name:")
    new_subject = simpledialog.askstring("Subject", "What subject is this pet for?") or "General"
    pet = Pet(name=new_name, subject=new_subject)
    db.save_pet_state(pet)

# Apply decay at launch
pet.apply_decay()
db.save_pet_state(pet)

# Reopen main window
root = tk.Tk()
root.title("Virtual Study Pet")
root.geometry("320x340")
root.resizable(False, False)

canvas = tk.Canvas(root, width=100, height=100, bg="lightgray")
canvas.pack(pady=5)

status_var = tk.StringVar()
status_var.set(pet.get_summary())
status_label = tk.Label(root, textvariable=status_var, justify=tk.LEFT)
status_label.pack(pady=5)

streak_var = tk.StringVar()
streak_var.set(f"Streak: {pet.streak} days")
streak_label = tk.Label(root, textvariable=streak_var)
streak_label.pack(pady=2)

decay_status_var = tk.StringVar()
decay_status_var.set("Decay: Active" if not pet.paused else "Decay: Paused")
decay_label = tk.Label(root, textvariable=decay_status_var)
decay_label.pack(pady=2)

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

button_frame = tk.Frame(root)
button_frame.pack(pady=5)
tk.Button(button_frame, text="Study", command=handle_study, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Feed", command=handle_feed, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Rest", command=handle_rest, width=8).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Play", command=handle_play, width=8).pack(side=tk.LEFT, padx=5)

tk.Button(root, text="Toggle Nap/Vacation", command=toggle_decay).pack(pady=5)

# Cleanup: close DB and window on exit
def on_close():
    db.save_pet_state(pet)
    db.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()

root.protocol("WM_DELETE_WINDOW", on_close)

# Start the Tkinter event loop
root.mainloop()
