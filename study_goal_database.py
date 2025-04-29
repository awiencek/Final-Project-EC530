import sqlite3

class StudyGoalDatabase:
    def __init__(self, db_name="study_buddy.db"):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """Create table to store study goals."""
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS study_goals (
            id INTEGER PRIMARY KEY,
            goal TEXT,
            completed BOOLEAN
        )
        """)
        self.conn.commit()

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

    def close(self):
        """Close the database connection."""
        self.conn.close()
