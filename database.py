import sqlite3
from datetime import datetime


class ReminderDB:
    def __init__(self, db_path="reminders.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS reminders
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                title
                                TEXT
                                NOT
                                NULL,
                                description
                                TEXT,
                                location
                                TEXT,
                                reminder_time
                                TEXT
                                NOT
                                NULL,
                                is_completed
                                INTEGER
                                DEFAULT
                                0,
                                created_at
                                TEXT
                                DEFAULT
                                CURRENT_TIMESTAMP
                            )
                            ''')
        self.conn.commit()

    def add_reminder(self, title, description, location, reminder_time):
        self.cursor.execute('''
                            INSERT INTO reminders (title, description, location, reminder_time)
                            VALUES (?, ?, ?, ?)
                            ''', (title, description, location, reminder_time))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_reminders(self):
        self.cursor.execute('SELECT * FROM reminders ORDER BY reminder_time ASC')
        return self.cursor.fetchall()

    def get_pending_reminders(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.cursor.execute('''
                            SELECT *
                            FROM reminders
                            WHERE reminder_time <= ?
                              AND is_completed = 0
                            ''', (now,))
        return self.cursor.fetchall()

    def mark_completed(self, reminder_id):
        self.cursor.execute('UPDATE reminders SET is_completed = 1 WHERE id = ?', (reminder_id,))
        self.conn.commit()

    def delete_reminder(self, reminder_id):
        self.cursor.execute('DELETE FROM reminders WHERE id = ?', (reminder_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()