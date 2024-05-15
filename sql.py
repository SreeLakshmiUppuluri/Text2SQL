import sqlite3

# Connect to SQLite
connection = sqlite3.connect("student.db")

# Create a cursor object to insert records and create tables
cursor = connection.cursor()

# Create the table if it doesn't exist
table_info = """
CREATE TABLE IF NOT EXISTS STUDENT (
    NAME VARCHAR(25),
    CLASS VARCHAR(25),
    SECTION VARCHAR(25),
    MARKS INT
);
"""
cursor.execute(table_info)

# Insert 50 additional records
records_to_insert = [
    ("John", "Data Science", "A", 75),
    ("Alice", "Machine Learning", "B", 80),
    ("Bob", "Data Science", "A", 90),
    ("Emma", "DEVOPS", "C", 85),
    ("Eva", "Machine Learning", "B", 95),
    ("Michael", "Data Science", "A", 88),
    ("Sophia", "Data Science", "B", 82),
    ("Liam", "Machine Learning", "C", 79),
    ("Olivia", "DEVOPS", "A", 87),
    ("Noah", "Machine Learning", "A", 93),
    ("Ava", "Data Science", "C", 81),
    ("William", "Machine Learning", "A", 94),
    ("Isabella", "Data Science", "B", 76),
    ("James", "DEVOPS", "C", 85),
    ("Charlotte", "Machine Learning", "A", 92),
    ("Benjamin", "Data Science", "A", 89),
    ("Amelia", "Machine Learning", "B", 83),
    ("Lucas", "DEVOPS", "B", 78),
    ("Mia", "Machine Learning", "C", 84),
    ("Henry", "Data Science", "A", 91),
    ("Evelyn", "Machine Learning", "A", 96),
    ("Alexander", "Data Science", "B", 77),
    ("Harper", "Machine Learning", "C", 86),
    ("Daniel", "DEVOPS", "A", 82),
    ("Sofia", "Machine Learning", "A", 97),
    ("Matthew", "Data Science", "C", 79),
    ("Aria", "Machine Learning", "B", 88),
    ("Jackson", "DEVOPS", "C", 81),
    ("Luna", "Machine Learning", "A", 98),
    ("David", "Data Science", "A", 90),
    ("Grace", "Machine Learning", "B", 87),
    ("Carter", "DEVOPS", "A", 80),
    ("Chloe", "Machine Learning", "C", 85),
    ("Wyatt", "Data Science", "B", 92),
    ("Zoe", "Machine Learning", "A", 99),
    ("John", "DEVOPS", "C", 83),
    ("Madison", "Machine Learning", "B", 86),
    ("Jayden", "Data Science", "A", 88),
    ("Nora", "Machine Learning", "A", 95),
    ("Elijah", "DEVOPS", "B", 82),
    ("Riley", "Machine Learning", "C", 84),
    ("Luke", "Data Science", "A", 89),
    ("Penelope", "Machine Learning", "A", 96),
    ("Oliver", "DEVOPS", "C", 81),
    ("Leah", "Machine Learning", "B", 88),
    ("Gabriel", "Data Science", "A", 90),
    ("Stella", "Machine Learning", "C", 87),
]

cursor.executemany("INSERT INTO STUDENT VALUES (?, ?, ?, ?)", records_to_insert)

# Display all the records
print("The inserted records are:")
data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    print(row)

# Commit changes to the database
connection.commit()
connection.close()
