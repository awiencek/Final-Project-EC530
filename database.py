import sqlite3
from datetime import datetime, date, timedelta

class StudyAppDB:
    def __init__(self, db_path="study_app.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS pet (
            name TEXT PRIMARY KEY,
            level INTEGER,
            experience INTEGER,
            hunger INTEGER,
            energy INTEGER,
            happiness INTEGER,
            streak INTEGER DEFAULT 0,
            last_goal_completed_at TEXT
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            completed BOOLEAN,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP
        )
        """)
        self.conn.commit()

    def save_pet_state(self, pet):
        self.cursor.execute("""
            UPDATE pet
            SET level=?, experience=?, hunger=?, energy=?, happiness=?, streak=?, last_goal_completed_at=?
            WHERE name=?
        """, (pet.level, pet.experience, pet.hunger, pet.energy, pet.happiness, pet.streak, pet.last_goal_completed_at, pet.name))

        if self.cursor.rowcount == 0:
            self.cursor.execute("""
                INSERT INTO pet (name, level, experience, hunger, energy, happiness, streak, last_goal_completed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (pet.name, pet.level, pet.experience, pet.hunger, pet.energy, pet.happiness, pet.streak, pet.last_goal_completed_at))

        self.conn.commit()

    def load_pet(self, name):
        self.cursor.execute("""
            SELECT name, level, experience, hunger, energy, happiness, streak, last_goal_completed_at
            FROM pet WHERE name=?
        """, (name,))
        row = self.cursor.fetchone()
        if row:
            return {
                "name": row[0],
                "level": row[1],
                "experience": row[2],
                "hunger": row[3],
                "energy": row[4],
                "happiness": row[5],
                "streak": row[6],
                "last_goal_completed_at": row[7]
            }
        return None

    def mark_goal_completed(self, goal_id, pet):
        now = datetime.now().isoformat()
        self.cursor.execute("""
            UPDATE study_goals SET completed=1, completed_at=? WHERE id=?
        """, (now, goal_id))

        # Streak logic
        today = date.today()
        last_str = pet.last_goal_completed_at
        if last_str:
            last_date = datetime.fromisoformat(last_str).date()
            if last_date == today:
                pass  # Already counted today
            elif last_date == today - timedelta(days=1):
                pet.streak += 1
            else:
                pet.streak = 1
        else:
            pet.streak = 1

        pet.last_goal_completed_at = now
        self.save_pet_state(pet)
        self.conn.commit()

    def get_all_goals(self):
        self.cursor.execute("SELECT * FROM study_goals")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
