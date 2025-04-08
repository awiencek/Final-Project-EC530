import sqlite3

class Database:
    def __init__(self, db_name="study_buddy.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create tables to store study goals, pet status, and achievements."""
        # Create table to store pet's current state (including experience and emotional state)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pet (
            id INTEGER PRIMARY KEY,
            happiness INTEGER,
            health INTEGER,
            hunger INTEGER,
            energy INTEGER,
            level INTEGER,
            experience INTEGER,
            achievements TEXT
        )
        """)
        # Create table to store study goals
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_goals (
            id INTEGER PRIMARY KEY,
            goal TEXT,
            completed BOOLEAN
        )
        """)
        # Commit changes to the database
        self.conn.commit()

    def save_pet_state(self, pet):
        """Save pet's current state (including achievements, experience, and emotional state) to the database."""
        achievements = ','.join(pet.achievements)  # Save achievements as a comma-separated string
        self.cursor.execute("""
        INSERT INTO pet (happiness, health, hunger, energy, level, experience, achievements)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pet.happiness, pet.health, pet.hunger, pet.energy, pet.level, pet.experience, achievements))
        self.conn.commit()

    def load_pet_state(self):
        """Load pet's most recent state from the database."""
        self.cursor.execute("SELECT * FROM pet ORDER BY id DESC LIMIT 1")
        result = self.cursor.fetchone()
        if result:
            # Convert achievements string back to a list
            achievements = result[7].split(',') if result[7] else []
            pet = VirtualPet()
            pet.happiness = result[1]
            pet.health = result[2]
            pet.hunger = result[3]
            pet.energy = result[4]
            pet.level = result[5]
            pet.experience = result[6]
            pet.achievements = achievements
            return pet
        return VirtualPet()  # Return a new VirtualPet object if no data is found

    def add_study_goal(self, goal):
        """Add a study goal to the database."""
        self.cursor.execute("INSERT INTO study_goals (goal, completed) VALUES (?, ?)", (goal, False))
        self.conn.commit()

    def mark_goal_completed(self, goal_id):
        """Mark a study goal as completed."""
        self.cursor.execute("UPDATE study_goals SET completed = ? WHERE id = ?", (True, goal_id))
        self.conn.commit()

    def get_all_study_goals(self):
        """Get all study goals from the database."""
        self.cursor.execute("SELECT * FROM study_goals")
        goals = self.cursor.fetchall()
        return [{'id': goal[0], 'goal': goal[1], 'completed': goal[2]} for goal in goals]


