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
            last_goal_completed_at TEXT,
            last_decay_check TEXT,
            paused BOOLEAN DEFAULT 0,
            subject TEXT
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
            SET level=?, experience=?, hunger=?, energy=?, happiness=?, streak=?,
                last_goal_completed_at=?, last_decay_check=?, paused=?, subject=?
            WHERE name=?
        """, (pet.level, pet.experience, pet.hunger, pet.energy, pet.happiness,
              pet.streak, pet.last_goal_completed_at, pet.last_decay_check, pet.paused, pet.subject, pet.name))

        if self.cursor.rowcount == 0:
            self.cursor.execute("""
                INSERT INTO pet (name, level, experience, hunger, energy, happiness, streak,
                                 last_goal_completed_at, last_decay_check, paused, subject)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (pet.name, pet.level, pet.experience, pet.hunger, pet.energy, pet.happiness,
                  pet.streak, pet.last_goal_completed_at, pet.last_decay_check, pet.paused, pet.subject))

        self.conn.commit()

    def load_pet(self, name):
        self.cursor.execute("""
            SELECT name, level, experience, hunger, energy, happiness, streak,
                   last_goal_completed_at, last_decay_check, paused, subject
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
                "last_goal_completed_at": row[7],
                "last_decay_check": row[8],
                "paused": bool(row[9]),
                "subject": row[10]
            }
        return None

    def list_pets(self):
        self.cursor.execute("SELECT name, subject FROM pet")
        return self.cursor.fetchall()

    def mark_goal_completed(self, goal_id, pet):
        now = datetime.now().isoformat()
        self.cursor.execute("""
            UPDATE study_goals SET completed=1, completed_at=? WHERE id=?
        """, (now, goal_id))

        today = date.today()
        last_str = pet.last_goal_completed_at
        if last_str:
            try:
                last_date = datetime.fromisoformat(last_str).date()
                if last_date == today - timedelta(days=1):
                    pet.streak += 1
                elif last_date != today:
                    pet.streak = 1
            except Exception:
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

    def update_pet_subject(self, name, new_subject):
        self.cursor.execute("UPDATE pet SET subject = ? WHERE name = ?", (new_subject, name))
        self.conn.commit()
