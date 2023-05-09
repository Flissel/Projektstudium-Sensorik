import psycopg2

# Connect to the PostgreSQL server
conn = psycopg2.connect(
    host="localhost",
    user="postgres",
    password="123",
    dbname="praktikum_db",
    port="5432",
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
        Rolle BOOLEAN
    );
''')

cur.execute('''
    CREATE TABLE IF NOT EXISTS public.multiplechoice_aufgaben
(
    id_multiplechoice_aufgaben integer NOT NULL,
    frage text COLLATE pg_catalog."default",
    option1 text COLLATE pg_catalog."default",
    option2 text COLLATE pg_catalog."default",
    option3 text COLLATE pg_catalog."default",
    option4 text COLLATE pg_catalog."default",
    antwort text COLLATE pg_catalog."default",
    CONSTRAINT multiplechoice_aufgaben_pkey PRIMARY KEY (id_multiplechoice_aufgaben)
)
    );
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS trainings (
  training_id SERIAL PRIMARY KEY,
  training_name TEXT,
  multiplechoice_question1_id INTEGER,
  multiplechoice_question2_id INTEGER,
  multiplechoice_question3_id INTEGER,
  multiplechoice_question4_id INTEGER,
  multiplechoice_question5_id INTEGER,
  multiplechoice_question6_id INTEGER,
  multiplechoice_question7_id INTEGER,
  multiplechoice_question8_id INTEGER,
  multiplechoice_question9_id INTEGER,
  multiplechoice_question10_id INTEGER,
	checkbox_question1_id INTEGER,
	checkbox_question2_id INTEGER,
	checkbox_question3_id INTEGER,
	checkbox_question4_id INTEGER,
	checkbox_question5_id INTEGER,
	checkbox_question6_id INTEGER,
	checkbox_question7_id INTEGER,
	checkbox_question8_id INTEGER,
	checkbox_question9_id INTEGER,
	checkbox_question10_id INTEGER,
	checkbox_grid_question1_id INTEGER,
	checkbox_grid_question2_id INTEGER,
	checkbox_grid_question3_id INTEGER,
	checkbox_grid_question4_id INTEGER,
	checkbox_grid_question5_id INTEGER,
	checkbox_grid_question6_id INTEGER,
	checkbox_grid_question7_id INTEGER,
	checkbox_grid_question8_id INTEGER,
	checkbox_grid_question9_id INTEGER,
	checkbox_grid_question10_id INTEGER,
	grid_question1_id INTEGER,
	grid_question2_id INTEGER,
	grid_question3_id INTEGER,
	grid_question4_id INTEGER,
	grid_question5_id INTEGER,
	grid_question6_id INTEGER,
	grid_question7_id INTEGER,
	grid_question8_id INTEGER,
	grid_question9_id INTEGER,
	grid_question10_id INTEGER,
	text_question1_id INTEGER,
	text_question2_id INTEGER,
	text_question3_id INTEGER,
	text_question4_id INTEGER,
	text_question5_id INTEGER,
	text_question6_id INTEGER,
	text_question7_id INTEGER,
	text_question8_id INTEGER,
	text_question9_id INTEGER,
	text_question10_id INTEGER,
	list_question1_id INTEGER,
	list_question2_id INTEGER,
	list_question3_id INTEGER,
	list_question4_id INTEGER,
	list_question5_id INTEGER,
	list_question6_id INTEGER,
	list_question7_id INTEGER,
	list_question8_id INTEGER,
	list_question9_id INTEGER,
	list_question10_id INTEGER
    )
    '''
)
# Add more CREATE TABLE statements for the other tables as needed

conn.commit()
cur.close()
conn.close()
