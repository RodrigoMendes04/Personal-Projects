import sqlite3

class JobDatabase:
    def __init__(self, db_name="jobs.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                company TEXT,
                url TEXT UNIQUE,
                sent BOOLEAN DEFAULT 0
            )
        ''')
        self.conn.commit()

    def job_exists(self, url):
        self.cursor.execute('SELECT 1 FROM jobs WHERE url = ?', (url,))
        return self.cursor.fetchone() is not None

    def add_job(self, title, company, url):
        try:
            self.cursor.execute('INSERT INTO jobs (title, company, url) VALUES (?, ?, ?)',
                                (title, company, url))
            self.conn.commit()
            print(f"[DB] New job saved: {title}")
        except sqlite3.IntegrityError:
            # URL already exists, skipping
            pass

    def close(self):
        self.conn.close()