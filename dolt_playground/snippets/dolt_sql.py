import mysql.connector

conn = mysql.connector.connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    password='hunter2'
)

cursor = conn.cursor()

db_name = 'state_persister'
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

conn.database = db_name

# Must be run in the same directory as the root of databases.
# In case of the assumed deployment it is /db.
cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INT,
    last_name VARCHAR(255),
    first_name VARCHAR(255),
    PRIMARY KEY (id)
)
""")

cursor.execute("SHOW TABLES")
print(cursor.fetchall())

cursor.execute("CALL dolt_add('employees')")
print(cursor.fetchall())

cursor.execute("CALL dolt_commit('-m', 'Created initial schema')")
print(cursor.fetchall())

cursor.execute("SELECT * FROM dolt_log")
print("=== Initial Commit Log ===")
for row in cursor.fetchall():
    print(row)

cursor.execute("""
INSERT INTO employees (id, last_name, first_name) VALUES
    (0, 'Sehn', 'Tim'),
    (1, 'Hendriks', 'Brian'),
    (2, 'Son', 'Aaron'),
    (3, 'Fitzgerald', 'Brian')
""")

cursor.execute("CALL dolt_commit('-am', 'Populated tables with data')")
print(cursor.fetchall())

cursor.execute("SELECT * FROM dolt_log")
print("\n=== Updated Commit Log ===")
for row in cursor.fetchall():
    print(row)

cursor.execute("SELECT * FROM dolt_diff_employees")
print("\n=== Dolt Diff ===")
for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()
