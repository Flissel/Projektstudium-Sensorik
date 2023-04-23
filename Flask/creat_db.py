import psycopg2

# Connect to the PostgreSQL server
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="123",
    dbname="praktikum_db",
   
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Create the necessary tables
cur = conn.cursor()
cur.execute('''
    CREATE TABLE if not Exists Aufgaben (
        ID_Aufgabe SERIAL PRIMARY KEY,
        Beschreibung TEXT,
        Antwort TEXT,
        Bewertung INTEGER,
        Praktikum_ID INTEGER 
    );
''')

cur.execute('''
    CREATE TABLE if not Exists Studenten (
        ID_Student SERIAL PRIMARY KEY,
        Name VARCHAR(50),
        Passwort VARCHAR(100),
        Anzahl_Aufgaben INTEGER DEFAULT 0,
        Praktikum_ID INTEGER 
    );
''')
cur.execute('''
    CREATE TABLE if not Exists Praktikum (
        ID_Praktikum SERIAL PRIMARY KEY,
        Beschreibung TEXT
    );
''')



cur.execute('''
    CREATE TABLE if not Exists Bewertungen (
        ID_Bewertung SERIAL PRIMARY KEY,
        Aufgabe_ID INTEGER ,
        Student_ID INTEGER ,
        Bewertung INTEGER
    );
''')

cur.execute('''
    CREATE TABLE if not Exists Benutzer (
        ID_Benutzer SERIAL PRIMARY KEY,
        Benutzername TEXT,
        Passwort TEXT,
        Rolle TEXT
    );
''')
# Add more CREATE TABLE statements for the other tables as needed

conn.commit()
cur.close()
conn.close()
