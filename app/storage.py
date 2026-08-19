import sqlite3
import json


DATABASE = "jobs.db"


def create_database():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT NOT NULL,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            url TEXT NOT NULL,
            description TEXT,
            tags TEXT,
            remote INTEGER,
            UNIQUE(source, id)
        )
    """)

    connection.commit()
    connection.close()


def save_jobs(jobs):
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    for job in jobs:

        cursor.execute("""
            INSERT OR IGNORE INTO jobs
            (id, source, title, company, location, url, description, tags, remote)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job["id"],
            job["source"],
            job["title"],
            job["company"],
            job.get("location"),
            job["url"],
            job.get("description"),
            json.dumps(job.get("tags", [])),
            int(job.get("remote", False))
        ))

    connection.commit()
    connection.close()
def get_all_jobs():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, source, title, company, location, url, remote
        FROM jobs
    """)

    rows = cursor.fetchall()

    connection.close()

    return rows