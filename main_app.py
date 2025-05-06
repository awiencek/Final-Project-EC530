import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from pet import Pet
from database import StudyAppDB
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize DB and fetch pet list
db = StudyAppDB()
pets = db.list_pets()
pet_names = [name for name, _ in pets]

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

pet.apply_decay()
db.save_pet_state(pet)

root = tk.Tk()
root.title("Virtual Study Pet")
root.geometry("380x480")
root.resizable(False, False)

style = ttk.Style()
style.theme_use("clam")

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(main_frame, width=120, height=100, bg="#eeeeee")
canvas.pack(pady=(0, 10))

status_var = tk.StringVar()
status_var.set(pet.get_summary())
status_label = ttk.Label(main_frame, textvariable=status_var, justify=tk.LEFT)
status_label.pack(pady=5)

streak_var = tk.StringVar()
streak_var.set(f"Streak: {pet.streak} days")
streak_label = ttk.Label(main_frame, textvariable=streak_var)
streak_label.pack()

decay_status_var = tk.StringVar()
decay_status_var.set("Decay: Active" if not pet.paused else "Decay: Paused")
decay_label = ttk.Label(main_frame, textvariable=decay_status_var)
decay_label.pack(pady=(0, 10))

def refresh_ui():
    status_var.set(pet.get_summary())
    streak_var.set(f"Streak: {pet.streak} days")
    decay_status_var.set("Decay: Active" if not pet.paused else "Decay: Paused")

def handle_study():
    pet.study()
    check_auto_achievements()
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

def edit_subject():
    new_subject = simpledialog.askstring("Edit Subject", "Enter a new subject for this pet:")
    if new_subject:
        pet.subject = new_subject
        db.update_pet_subject(pet.name, new_subject)
        refresh_ui()

def unlock_achievement():
    name = simpledialog.askstring("Unlock Achievement", "Enter achievement name:")
    if name:
        if name not in pet.achievements:
            pet.achievements.append(name)
            messagebox.showinfo("Achievement", f"Unlocked: {name}!")
            db.save_pet_state(pet)
            refresh_ui()
        else:
            messagebox.showinfo("Achievement", f"Already unlocked: {name}")

def check_auto_achievements():
    if pet.level >= 5 and "Scholar" not in pet.achievements:
        pet.achievements.append("Scholar")
        messagebox.showinfo("Achievement", "Unlocked: Scholar!")
    if pet.streak >= 7 and "Consistent" not in pet.achievements:
        pet.achievements.append("Consistent")
        messagebox.showinfo("Achievement", "Unlocked: Consistent!")

def show_achievements():
    if pet.achievements:
        messagebox.showinfo("Achievements", "Unlocked Achievements:\n" + "\n".join(pet.achievements))
    else:
        messagebox.showinfo("Achievements", "No achievements unlocked yet.")

def view_study_history():
    goals = db.get_all_goals()
    counts = defaultdict(int)
    for goal in goals:
        if goal[2] and goal[4]:  # completed and has completed_at
            date_str = goal[4][:10]  # YYYY-MM-DD
            counts[date_str] += 1

    if not counts:
        messagebox.showinfo("History", "No study goals completed yet.")
        return

    dates = sorted(counts.keys())
    values = [counts[d] for d in dates]

    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.bar(dates, values, color="#4CAF50")
    ax.set_title("Study Goals Completed by Day")
    ax.set_xlabel("Date")
    ax.set_ylabel("Goals")
    ax.set_xticklabels(dates, rotation=45, ha='right')
    fig.tight_layout()

    chart_window = tk.Toplevel(root)
    chart_window.title("Study History")

    canvas_chart = FigureCanvasTkAgg(fig, master=chart_window)
    canvas_chart.draw()
    canvas_chart.get_tk_widget().pack()

    description = "\n".join([f"{d}: {c} goal(s)" for d, c in zip(dates, values)])
    ttk.Label(chart_window, text=description, justify=tk.LEFT, padding=5).pack()

button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=10)

btn_opts = {"width": 12, "padding": 5}

ttk.Button(button_frame, text="Study", command=handle_study, **btn_opts).grid(row=0, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Feed", command=handle_feed, **btn_opts).grid(row=0, column=1, padx=5, pady=5)
ttk.Button(button_frame, text="Rest", command=handle_rest, **btn_opts).grid(row=1, column=0, padx=5, pady=5)
ttk.Button(button_frame, text="Play", command=handle_play, **btn_opts).grid(row=1, column=1, padx=5, pady=5)

control_frame = ttk.Frame(main_frame)
control_frame.pack(pady=10)

ttk.Button(control_frame, text="Toggle Nap/Vacation", command=toggle_decay, width=28).pack(pady=4)
ttk.Button(control_frame, text="Edit Subject", command=edit_subject, width=28).pack(pady=4)
ttk.Button(control_frame, text="Unlock Achievement", command=unlock_achievement, width=28).pack(pady=4)
ttk.Button(control_frame, text="View Achievements", command=show_achievements, width=28).pack(pady=4)
ttk.Button(control_frame, text="View Study History", command=view_study_history, width=28).pack(pady=4)

def on_close():
    db.save_pet_state(pet)
    db.close()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
root.mainloop()
