# database.py
import sqlite3

class Database:
    def __init__(self, db_name="study_buddy.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create tables to store study goals and pet status."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pet (
            id INTEGER PRIMARY KEY,
            happiness INTEGER,
            health INTEGER,
            hunger INTEGER,
            energy INTEGER,
            level INTEGER
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_goals (
            id INTEGER PRIMARY KEY,
            goal TEXT,
            completed BOOLEAN
        )
        """)
        self.conn.commit()

    def save_pet_status(self, pet):
        """Save pet's current status to the database."""
        self.cursor.execute("""
        INSERT INTO pet (happiness, health, hunger, energy, level)
        VALUES (?, ?, ?, ?, ?)
        """, (pet.happiness, pet.health, pet.hunger, pet.energy, pet.level))
        self.conn.commit()

    def get_pet_status(self):
        """Get pet's current status from the database."""
        self.cursor.execute("SELECT * FROM pet ORDER BY id DESC LIMIT 1")
        result = self.cursor.fetchone()
        if result:
            return {
                'happiness': result[1],
                'health': result[2],
                'hunger': result[3],
                'energy': result[4],
                'level': result[5]
            }
        return None

    def add_study_goal(self, goal):
        """Add a study goal."""
        self.cursor.execute("INSERT INTO study_goals (goal, completed) VALUES (?, ?)", (goal, False))
        self.conn.commit()

    def mark_goal_completed(self, goal_id):
        """Mark a study goal as completed."""
        self.cursor.execute("UPDATE study_goals SET completed = ? WHERE id = ?", (True, goal_id))
        self.conn.commit()
