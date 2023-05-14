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

-- Create the aufgabenstellungen table
CREATE TABLE aufgabenstellungen (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    aufgabentyp TEXT NOT NULL
);
            
-- Create the Trainings table
CREATE TABLE trainings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    fragen_id_1 INTEGER,
    fragen_id_2 INTEGER,
    fragen_id_3 INTEGER,
    fragen_id_4 INTEGER,
    fragen_id_5 INTEGER,
    fragen_id_6 INTEGER,
    fragen_id_7 INTEGER,
    fragen_id_8 INTEGER,
    fragen_id_9 INTEGER,
    fragen_id_10 INTEGER,
    FOREIGN KEY (fragen_id_1) REFERENCES fragen (id) ON DELETE CASCADE,
    FOREIGN KEY (fragen_id_2) REFERENCES fragen (id) ON DELETE CASCADE,
    FOREIGN KEY (fragen_id_3) REFERENCES fragen (id) ON DELETE CASCADE,
    FOREIGN KEY (fragen_id_4) REFERENCES fragen (id) ON DELETE CASCADE,
    FOREIGN KEY (fragen_id_5) REFERENCES fragen (id) ON DELETE CASCADE,
    FOREIGN KEY (fragen_id_6) REFERENCES fragen (id) ON DELETE CASCADE,
    FOREIGN KEY (fragen_id_7) REFERENCES fragen (id) ON DELETE CASCADE,
    FOREIGN KEY (fragen_id_8) REFERENCES fragen (id) ON DELETE CASCADE,
    FOREIGN KEY (fragen_id_9) REFERENCES fragen (id) ON DELETE CASCADE,
    FOREIGN KEY (fragen_id_10) REFERENCES fragen (id) ON DELETE CASCADE
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
    proben_id_1 INTEGER NOT NULL,
    proben_id_2 INTEGER NOT NULL,
    proben_id_3 INTEGER NOT NULL,
    proben_id_4 INTEGER NOT NULL,
    proben_id_5 INTEGER NOT NULL,
    proben_id_6 INTEGER NOT NULL,
    proben_id_7 INTEGER NOT NULL,
    proben_id_8 INTEGER NOT NULL,
    proben_id_9 INTEGER NOT NULL,
    proben_id_10 INTEGER NOT NULL,
    FOREIGN KEY (proben_id_1) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_2) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_3) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_4) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_5) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_6) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_7) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_8) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_9) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_10) REFERENCES proben (id) ON DELETE CASCADE
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
    title_id INTEGER,
    prüfvariante TEXT NOT NULL,
    probenreihe_id INTEGER NOT NULL,
    proben_auswahl INTEGER,
    beschreibung TEXT,
    FOREIGN KEY (probenreihe_id) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (title_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the konz_reihe table
CREATE TABLE konz_reihe (
    id SERIAL PRIMARY KEY,
    title_id INTEGER,
    probenreihe_id INTEGER NOT NULL,
    probe_1_antwort TEXT,
    probe_2_antwort TEXT,
    probe_3_antwort TEXT,
    probe_4_antwort TEXT,
    probe_5_antwort TEXT,
    probe_6_antwort TEXT,
    probe_7_antwort TEXT,
    probe_8_antwort TEXT,
    probe_9_antwort TEXT,
    probe_10_antwort TEXT,

    FOREIGN KEY (probenreihe_id) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (title_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the profilprüfung table
CREATE TABLE profilprüfung (
    id SERIAL PRIMARY KEY,
    title_id INTEGER,
    proben_id INTEGER NOT NULL,
    kriterium_1 TEXT,
    kriterium_2 TEXT,
    kriterium_3 TEXT,
    kriterium_4 TEXT,
    kriterium_5 TEXT,
    kriterium_6 TEXT,
    kriterium_7 TEXT,
    kriterium_8 TEXT,
    kriterium_9 TEXT,
    skalenbewertung_1 INTEGER,
    skalenbewertung_2 INTEGER,
    skalenbewertung_3 INTEGER,
    skalenbewertung_4 INTEGER,
    skalenbewertung_5 INTEGER,
    skalenbewertung_6 INTEGER,
    skalenbewertung_7 INTEGER,
    skalenbewertung_8 INTEGER,
    skalenbewertung_9 INTEGER,
    FOREIGN KEY (proben_id) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (title_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the hedonische_beurteilung table
CREATE TABLE hed_beurteilung (
    id SERIAL PRIMARY KEY,
    title_id INTEGER,
    proben_id INTEGER NOT NULL,
    beurteilung TEXT,
    anmerkung TEXT,
    FOREIGN KEY (proben_id) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (title_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the auswahltest table
CREATE TABLE auswahltest (
    id SERIAL PRIMARY KEY,
    title_id INTEGER,
    prüfvariante TEXT NOT NULL,
    proben_id_1 INTEGER NOT NULL,
    proben_id_2 INTEGER NOT NULL,
    proben_id_3 INTEGER NOT NULL,
    proben_id_4 INTEGER NOT NULL,
    proben_id_5 INTEGER NOT NULL,
    proben_id_6 INTEGER NOT NULL,
    bemerkung_1 TEXT,
    bemerkung_2 TEXT,
    bemerkung_3 TEXT,
    bemerkung_4 TEXT,
    bemerkung_5 TEXT,
    bemerkung_6 TEXT,
    FOREIGN KEY (proben_id_1) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_2) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_3) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_4) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_5) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_6) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (title_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the geruchserkennung table
CREATE TABLE geruchserkennung (
    id SERIAL PRIMARY KEY,
    title_id INTEGER,
    proben_id INTEGER NOT NULL,
    geruch_ohne_auswahl TEXT,
    geruch_mit_auswahl TEXT,
    bemerkung TEXT,
    FOREIGN KEY (proben_id) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (title_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the paar_vergleich table
CREATE TABLE paar_vergleich (
    id SERIAL PRIMARY KEY,
    title_id INTEGER,
    prüfvariante TEXT NOT NULL,
    proben_id_1 INTEGER NOT NULL,
    proben_id_2 INTEGER NOT NULL,
    proben_auswahl_id TEXT,
    bemerkung TEXT,
    FOREIGN KEY (proben_id_1) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (proben_id_2) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (title_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the EBP table
CREATE TABLE ebp (
    id SERIAL PRIMARY KEY,
    title_id INTEGER,
    prüfvariante TEXT,
    proben_id INTEGER NOT NULL,
    aussehen_farbe TEXT,
    geruch TEXT,
    geschmack TEXT,
    textur TEXT,
    konsistenz TEXT,
    FOREIGN KEY (proben_id) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (title_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the rangordnungstest table
CREATE TABLE rangordnungstest (
    id SERIAL PRIMARY KEY,
    title_id INTEGER,
    prüfvariante TEXT NOT NULL,
    probenreihe_id INTEGER NOT NULL,
    rang_1_proben_id INTEGER,
    rang_2_proben_id INTEGER,
    rang_3_proben_id INTEGER,
    rang_4_proben_id INTEGER,
    rang_5_proben_id INTEGER,
    FOREIGN KEY (probenreihe_id) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (title_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Add foreign key constraints for the fragens table

ALTER TABLE fragen
ADD CONSTRAINT fk_fragen_ebp
FOREIGN KEY (fragen_id)
REFERENCES ebp (id)
ON DELETE CASCADE;

ALTER TABLE fragen
ADD CONSTRAINT fk_fragen_rangordnungstest
FOREIGN KEY (fragen_id)
REFERENCES rangordnungstest (id)
ON DELETE CASCADE;

ALTER TABLE fragen
ADD CONSTRAINT fk_fragen_paar_vergleich
FOREIGN KEY (fragen_id)
REFERENCES paar_vergleich (id)
ON DELETE CASCADE;

ALTER TABLE fragen
ADD CONSTRAINT fk_fragen_geruchserkennung
FOREIGN KEY (fragen_id)
REFERENCES geruchserkennung (id)
ON DELETE CASCADE;

ALTER TABLE fragen
ADD CONSTRAINT fk_fragen_auswahltest
FOREIGN KEY (fragen_id)
REFERENCES auswahltest (id)
ON DELETE CASCADE;

ALTER TABLE fragen
ADD CONSTRAINT fk_fragen_hed_beurteilung
FOREIGN KEY (fragen_id)
REFERENCES hed_beurteilung (id)
ON DELETE CASCADE;

ALTER TABLE fragen
ADD CONSTRAINT fk_fragen_profilprüfung
FOREIGN KEY (fragen_id)
REFERENCES profilprüfung (id)
ON DELETE CASCADE;

ALTER TABLE fragen
ADD CONSTRAINT fk_fragen_konz_reihe
FOREIGN KEY (fragen_id)
REFERENCES konz_reihe (id)
ON DELETE CASCADE;

ALTER TABLE fragen
ADD CONSTRAINT fk_fragen_dreieckstest
FOREIGN KEY (fragen_id)
REFERENCES dreieckstest (id)
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
	id, proben_nr, probenname, farbe, farbintensität, geruch, geschmack, textur, konsistenz)
	VALUES (1, 999, 'Schwarzdorn', 'Schwarz', 100, 'erdig', 'salzig', 'rau', 'fest');

            
            
            
            
            ''')


conn.commit()
cur.close()
conn.close()
