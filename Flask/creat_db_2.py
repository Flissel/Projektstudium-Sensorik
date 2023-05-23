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
cur.execute('''
DROP TABLE IF EXISTS paar_vergleich CASCADE;
DROP TABLE IF EXISTS profilprüfung CASCADE;
DROP TABLE IF EXISTS konz_reihe CASCADE;
DROP TABLE IF EXISTS dreieckstest CASCADE;
DROP TABLE IF EXISTS benutzer CASCADE;
DROP TABLE IF EXISTS probenreihen CASCADE;
DROP TABLE IF EXISTS proben CASCADE;
DROP TABLE IF EXISTS trainings CASCADE;
DROP TABLE IF EXISTS aufgabenstellungen CASCADE;
DROP TABLE IF EXISTS prüfvarianten CASCADE;
DROP TABLE IF EXISTS fragen CASCADE;
DROP TABLE IF EXISTS fragen_trainings CASCADE;
''')
# Create the necessary tables

# TODO: Complete tables in the database

cur.execute('''
-- Create the Fragen table
CREATE TABLE fragen (
    id SERIAL PRIMARY KEY,
    fragen_typ VARCHAR(255) NOT NULL,
    fragen_id INTEGER NOT NULL
);

-- Create the prüfvarianten table
CREATE TABLE prüfvarianten (
    id SERIAL PRIMARY KEY,
    prüfname TEXT
);

-- Create the aufgabenstellungen table
CREATE TABLE aufgabenstellungen (
    id SERIAL PRIMARY KEY,
    aufgabenstellung TEXT NOT NULL,
    aufgabentyp TEXT NOT NULL,
    prüfvarianten_id INTEGER,
    FOREIGN KEY (prüfvarianten_id) REFERENCES prüfvarianten (id) ON DELETE CASCADE
);

CREATE TABLE trainings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    reference TEXT[]  -- array that saves question type and ID as string or number
);

-- Create the Fragen_Trainings table
CREATE TABLE fragen_trainings (
    id SERIAL PRIMARY KEY,
    fragen_id INTEGER NOT NULL,
    trainings_id INTEGER NOT NULL,
    FOREIGN KEY (fragen_id) REFERENCES fragen (id) ON DELETE CASCADE,
    FOREIGN KEY (trainings_id) REFERENCES trainings (id) ON DELETE CASCADE
);

-- Create the Proben table
CREATE TABLE proben (
    id SERIAL PRIMARY KEY,
    proben_nr INTEGER UNIQUE NOT NULL,
    probenname VARCHAR(255) NOT NULL,
    farbe TEXT,
    farbintensität INTEGER,
    geruch TEXT,
    geschmack TEXT,
    textur TEXT,
    konsistenz TEXT
);

-- Create the probenreihen table
CREATE TABLE probenreihen (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    proben_id INTEGER,
    FOREIGN KEY (proben_id) REFERENCES proben (id) ON DELETE CASCADE
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

-- Create the dreieckstest table
CREATE TABLE dreieckstest (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    probenreihe_id INTEGER NOT NULL,
    proben_auswahl INTEGER[],
    beschreibung TEXT,
    FOREIGN KEY (probenreihe_id) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the konz_reihe table
CREATE TABLE konz_reihe (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    probenreihe_id INTEGER NOT NULL,
    antworten TEXT[],
    FOREIGN KEY (probenreihe_id) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the profilprüfung table
CREATE TABLE profilprüfung (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    proben_id INTEGER NOT NULL,
    kriterien TEXT[],
    bewertungen TEXT[],
    FOREIGN KEY (proben_id) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the paar_vergleich table
CREATE TABLE paar_vergleich (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    proben_id_1 INTEGER NOT NULL,
    proben_id_2 INTEGER NOT NULL,
    beschreibung TEXT,
    FOREIGN KEY (proben_id_1) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_2) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);
''')

# Insert data into the fragen table
cur.execute('''
INSERT INTO fragen(fragen_typ, fragen_id)
VALUES 
    ('multiple_choice', 1),
    ('essay', 2),
    ('true_false', 3);
''')

# Insert data into the prüfvarianten table
cur.execute('''
INSERT INTO prüfvarianten(prüfname)
VALUES 
    ('prüfvariante1'),
    ('prüfvariante2');
''')

# Insert data into the aufgabenstellungen table
cur.execute('''
INSERT INTO aufgabenstellungen(aufgabenstellung, aufgabentyp, prüfvarianten_id)
VALUES 
    ('Was ist die Hauptstadt von Deutschland?', 'multiple_choice', 1),
    ('Schreiben Sie einen kurzen Aufsatz über Ihr Lieblingstier.', 'essay', NULL),
    ('Ist die Erde eine Scheibe?', 'true_false', 2);
''')

# Insert data into the trainings table
cur.execute('''
INSERT INTO trainings(name)
VALUES
    ('Training1'),
    ('Training2');
''')

# Insert data into the fragen_trainings table
cur.execute('''
INSERT INTO fragen_trainings(fragen_id, trainings_id)
VALUES
    (1, 1),
    (2, 1),
    (3, 2);
''')

# Insert data into the proben table
cur.execute('''
INSERT INTO proben(proben_nr, probenname, farbe, farbintensität, geruch, geschmack, textur, konsistenz)
VALUES
    (1, 'Probenname1', 'blau', 10, 'fruchtig', 'süß', 'weich', 'cremig'),
    (2, 'Probenname2', 'rot', 5, 'blumig', 'herb', 'hart', 'knusprig');
''')

# Insert data into the probenreihen table
cur.execute('''
INSERT INTO probenreihen(name, proben_id)
VALUES
    ('Probenreihe1', 1),
    ('Probenreihe2', 2);
''')

# Insert data into the benutzer table
cur.execute('''
INSERT INTO benutzer(benutzername, passwort, rolle, training_id)
VALUES
    ('Test', '123', TRUE, 1),
    ('Student1', '123', False, 1),
    ('Student2', '123', False, NULL),
    ('Student3', '123', False, NULL);
''')

# Commit the changes to the database
conn.commit()

# Close communication with the database
cur.close()
conn.close()
