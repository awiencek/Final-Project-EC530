# database.py
import sqlite3

class StudyAppDB:
    def __init__(self, db_path="study_app.db"):
        """Initialize connection to the SQLite database and ensure tables exist."""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create the pet and study_goals tables if they do not already exist."""
        # Pet table: name is primary key (assuming one pet per name)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pet (
            name TEXT PRIMARY KEY,
            level INTEGER,
            experience INTEGER,
            hunger INTEGER,
            energy INTEGER,
            happiness INTEGER
        )
        """)
        # Study goals table: auto-increment ID, description, completion status, timestamp
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            completed BOOLEAN,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.conn.commit()

    def save_pet_state(self, pet):
        """Save or update the pet's state in the database. Uses UPDATE or INSERT as needed."""
        # Try to update an existing pet record
        self.cursor.execute("""
            UPDATE pet
            SET level = ?, experience = ?, hunger = ?, energy = ?, happiness = ?
            WHERE name = ?
        """, (pet.level, pet.experience, pet.hunger, pet.energy, pet.happiness, pet.name))
        if self.cursor.rowcount == 0:
            # Pet not in DB, insert as new record
            self.cursor.execute("""
                INSERT INTO pet (name, level, experience, hunger, energy, happiness)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (pet.name, pet.level, pet.experience, pet.hunger, pet.energy, pet.happiness))
        self.conn.commit()

    def load_pet(self, name):
        """Load pet data by name. Returns a dict of pet attributes or None if not found."""
        self.cursor.execute("""
            SELECT name, level, experience, hunger, energy, happiness
            FROM pet
            WHERE name = ?
        """, (name,))
        row = self.cursor.fetchone()
        if row:
            return {
                "name": row[0],
                "level": row[1],
                "experience": row[2],
                "hunger": row[3],
                "energy": row[4],
                "happiness": row[5]
            }
        return None

    def add_goal(self, description):
        """Add a new study goal (initially not completed). Returns the new goal's ID."""
        self.cursor.execute("""
            INSERT INTO study_goals (description, completed)
            VALUES (?, 0)
        """, (description,))
        self.conn.commit()
        return self.cursor.lastrowid

    def mark_goal_completed(self, goal_id):
        """Mark a study goal as completed (completed = 1)."""
        self.cursor.execute("""
            UPDATE study_goals
            SET completed = 1
            WHERE id = ?
        """, (goal_id,))
        self.conn.commit()

    def delete_goal(self, goal_id):
        """Delete a study goal by its ID."""
        self.cursor.execute("DELETE FROM study_goals WHERE id = ?", (goal_id,))
        self.conn.commit()

    def clear_completed_goals(self):
        """Remove all goals that have been marked as completed."""
        self.cursor.execute("DELETE FROM study_goals WHERE completed = 1")
        self.conn.commit()

    def close(self):
        """Close the database connection."""
        self.conn.close()
