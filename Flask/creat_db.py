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

# TODO: Tabellen in der Datenbank vervollständigen

cur = conn.cursor()
cur.execute('''
            
-- Create the Fragen table
CREATE TABLE fragen (
    id SERIAL PRIMARY KEY,
    fragen_typ VARCHAR(255) NOT NULL,
    fragen_id INTEGER NOT NULL
);
            
-- Create the Trainings table
CREATE TABLE trainings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    question_id_1 INTEGER,
    question_id_2 INTEGER,
    question_id_3 INTEGER,
    question_id_4 INTEGER,
    question_id_5 INTEGER,
    question_id_6 INTEGER,
    question_id_7 INTEGER,
    question_id_8 INTEGER,
    question_id_9 INTEGER,
    question_id_10 INTEGER,
    FOREIGN KEY (question_id_1) REFERENCES questions (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id_2) REFERENCES questions (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id_3) REFERENCES questions (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id_4) REFERENCES questions (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id_5) REFERENCES questions (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id_6) REFERENCES questions (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id_7) REFERENCES questions (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id_8) REFERENCES questions (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id_9) REFERENCES questions (id) ON DELETE CASCADE,
    FOREIGN KEY (question_id_10) REFERENCES questions (id) ON DELETE CASCADE
);
            -- Create the Proben table
CREATE TABLE proben (
    id SERIAL PRIMARY KEY,
    proben_nr INTEGER UNIQUE NOT NULL,
    probenname VARCHAR(255) NOT NULL,
    aussehen_farbe TEXT NOT NULL,
    geruch TEXT NOT NULL,
    geschmack TEXT NOT NULL,
    textur TEXT NOT NULL,
    konsistenz TEXT NOT NULL
);

-- Create the Benutzer table
CREATE TABLE benutzer (
    id SERIAL PRIMARY KEY,
    benutzername TEXT NOT NULL,
    passwort TEXT NOT NULL,
    rolle BOOLEAN NOT NULL,
    training_id INTEGER,
    FOREIGN KEY (training_id) REFERENCES trainings (id) ON DELETE CASCADE
);

-- Create the EBP table
CREATE TABLE ebp (
    id SERIAL PRIMARY KEY,
    proben_id INTEGER NOT NULL,
    aussehen_farbe TEXT,
    geruch TEXT,
    geschmack TEXT,
    textur TEXT,
    konsistenz TEXT,
    FOREIGN KEY (proben_id) REFERENCES proben (id) ON DELETE CASCADE
);

-- Create the Rangordnungstest table
CREATE TABLE rangordnungstest (
    id SERIAL PRIMARY KEY,
    proben_id_1 INTEGER NOT NULL,
    proben_id_2 INTEGER NOT NULL,
    proben_id_3 INTEGER NOT NULL,
    proben_id_4 INTEGER NOT NULL,
    proben_id_5 INTEGER NOT NULL,
    FOREIGN KEY (proben_id_1) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_2) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_3) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_4) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_5) REFERENCES proben (id) ON DELETE CASCADE
);

-- Add foreign key constraints for the Questions table
ALTER TABLE questions
ADD CONSTRAINT fk_questions_ebp
FOREIGN KEY (question_id)
REFERENCES ebp (id)
ON DELETE CASCADE;

ALTER TABLE questions
ADD CONSTRAINT fk_questions_rangordnungstest
FOREIGN KEY (question_id)
REFERENCES rangordnungstest (id)
ON DELETE CASCADE;





INSERT INTO public.benutzer(
	id, benutzername, passwort, rolle, training_id)
	VALUES (1, 'Test', '123', TRUE, NULL);

INSERT INTO public.benutzer(
	id, benutzername, passwort, rolle, training_id)
	VALUES (2, 'Student1', '123', False, NULL);

INSERT INTO public.benutzer(
	id, benutzername, passwort, rolle, training_id)
	VALUES (3, 'Student2', '123', False, NULL);

INSERT INTO public.benutzer(
	id, benutzername, passwort, rolle, training_id)
	VALUES (4, 'Student3', '123', False, NULL);

INSERT INTO public.proben(
	id, proben_nr, probenname, aussehen_farbe, geruch, geschmack, textur, konsistenz)
	VALUES (1, 999, 'Schwarzdorn', 'Schwarz', 'erdig', 'salzig', 'rau', 'fest');

            
            
            
            
            ''')


conn.commit()
cur.close()
conn.close()
