import sqlite3
from faker import Faker
import random


conn = sqlite3.connect('university.db')
cur = conn.cursor()


cur.execute('''
    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        group_id INTEGER,
        FOREIGN KEY (group_id) REFERENCES groups(id)
    )
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        grade INTEGER,
        date TEXT,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
    )
''')

fake = Faker()

groups = ['Group A', 'Group B', 'Group C']
for group in groups:
    cur.execute("INSERT INTO groups (name) VALUES (?)", (group,))

for _ in range(5):
    cur.execute("INSERT INTO teachers (name) VALUES (?)", (fake.name(),))


subject_names = ['Math', 'Science', 'Literature', 'History', 'Art']
for subject in subject_names:
    teacher_id = random.randint(1, 5)
    cur.execute("INSERT INTO subjects (name, teacher_id) VALUES (?, ?)", (subject, teacher_id))


for _ in range(50):
    name = fake.name()
    group_id = random.randint(1, 3)
    cur.execute("INSERT INTO students (name, group_id) VALUES (?, ?)", (name, group_id))


for _ in range(1000):
    student_id = random.randint(1, 50)
    subject_id = random.randint(1, 5)
    grade = random.randint(1, 100)
    date = fake.date_this_year().isoformat()  # Форматування дати у форматі ISO 8601
    cur.execute("INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)", (student_id, subject_id, grade, date))

conn.commit()
cur.close()
conn.close()
