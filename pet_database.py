import sqlite3
from pet import VirtualPet

class PetDatabase:
    def __init__(self, db_name="study_buddy.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create table to store pet's state."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pet_state (
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
        self.conn.commit()

    def save_pet_state(self, pet):
        """Save the pet's state to the database."""
        achievements = ','.join(pet.achievements)
        self.cursor.execute("""
        INSERT INTO pet_state (happiness, health, hunger, energy, level, experience, achievements)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pet.happiness, pet.health, pet.hunger, pet.energy, pet.level, pet.experience, achievements))
        self.conn.commit()

    def load_pet_state(self):
        """Load the pet's most recent state from the database."""
        self.cursor.execute("SELECT * FROM pet_state ORDER BY id DESC LIMIT 1")
        row = self.cursor.fetchone()
        if row:
            pet = VirtualPet()
            pet.happiness, pet.health, pet.hunger, pet.energy, pet.level, pet.experience = row[1:7]
            pet.achievements = row[7].split(',') if row[7] else []
            return pet
        return VirtualPet()  # Return a new pet if no data is found

    def close(self):
        """Close the database connection."""
        self.conn.close()
