#!/usr/bin/env python
from database.db import get_db, init_db, seed_db

print("Initializing database...")
init_db()

print("Seeding database...")
seed_db()

db = get_db()

print("\n=== Users ===")
users = db.execute('SELECT * FROM users').fetchall()
for u in users:
    print(f"  ID {u['id']}: {u['name']} ({u['email']})")

print("\n=== Expenses ===")
expenses = db.execute('SELECT * FROM expenses').fetchall()
for e in expenses:
    print(f"  ID {e['id']}: ₹{e['amount']} - {e['category']} on {e['date']} (user {e['user_id']})")

print(f"\nTotal: {len(users)} users, {len(expenses)} expenses")

print("\n=== Testing Constraints ===")

try:
    db.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
               ('Duplicate', 'demo@spendly.com', 'xxx'))
    db.commit()
    print("ERROR: Duplicate email was allowed (constraint failed!)")
except Exception as e:
    print(f"✓ Unique email constraint works: {type(e).__name__}")

try:
    db.execute('INSERT INTO expenses (user_id, amount, category, date) VALUES (?, ?, ?, ?)',
               (999, 100, 'Food', '2026-05-01'))
    db.commit()
    print("ERROR: Invalid user_id was allowed (foreign key failed!)")
except Exception as e:
    print(f"✓ Foreign key constraint works: {type(e).__name__}")

db.close()
print("\n✓ Database setup complete!")
