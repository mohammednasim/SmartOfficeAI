import sqlite3
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

DATABASE_PATH = os.path.join(
    BASE_DIR,
    "database",
    "office.db"
)


connection = sqlite3.connect(DATABASE_PATH)

cursor = connection.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS employees(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    department TEXT,

    salary INTEGER
)
""")


cursor.execute("DELETE FROM employees")


cursor.executemany(
    """
    INSERT INTO employees(name, department, salary)
    VALUES (?, ?, ?)
    """,
    [
        ("Nasim", "AI", 70000),
        ("Rahul", "HR", 45000),
        ("Anu", "Finance", 60000),
        ("Arjun", "IT", 80000),
        ("Nisha", "Marketing", 55000)
    ]
)


connection.commit()
connection.close()

print("Database Created Successfully.")