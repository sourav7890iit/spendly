import sqlite3
import os
from werkzeug.security import generate_password_hash


def get_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'expense_tracker.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    db = get_db()
    db.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            name          TEXT    NOT NULL,
            email         TEXT    UNIQUE NOT NULL,
            password_hash TEXT    NOT NULL,
            created_at    TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL REFERENCES users(id),
            amount      REAL    NOT NULL,
            category    TEXT    NOT NULL,
            date        TEXT    NOT NULL,
            description TEXT,
            created_at  TEXT    DEFAULT (datetime('now'))
        );
    ''')
    db.commit()
    db.close()


def seed_db():
    db = get_db()

    user_count = db.execute('SELECT COUNT(*) FROM users').fetchone()[0]
    if user_count > 0:
        db.close()
        return

    user_id = db.execute(
        'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
        ('Demo User', 'demo@spendly.com', generate_password_hash('demo123'))
    ).lastrowid

    expenses = [
        (user_id, 4500.00, 'Bills', '2026-05-01', 'Monthly rent'),
        (user_id, 850.00, 'Food', '2026-05-03', 'Grocery shopping'),
        (user_id, 320.00, 'Transport', '2026-05-05', 'Monthly bus pass'),
        (user_id, 1200.00, 'Health', '2026-05-08', 'Doctor consultation'),
        (user_id, 599.00, 'Entertainment', '2026-05-10', 'Netflix + Spotify'),
        (user_id, 2200.00, 'Shopping', '2026-05-12', 'New shoes'),
        (user_id, 450.00, 'Food', '2026-05-15', 'Restaurant dinner'),
        (user_id, 750.00, 'Other', '2026-05-18', 'Miscellaneous'),
    ]

    db.executemany(
        'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
        expenses
    )
    db.commit()
    db.close()
