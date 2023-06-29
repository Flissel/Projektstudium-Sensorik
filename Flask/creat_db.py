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

-- Drop all existing tables
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

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

-- Create the Trainings table
CREATE TABLE trainings (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    fragen_ids INTEGER[],
    fragen_typen TEXT[]

);

-- Create the Proben table
CREATE TABLE proben (
    id SERIAL PRIMARY KEY,
    proben_nr INTEGER UNIQUE NOT NULL,
    probenname VARCHAR(255) NOT NULL,
    farbe TEXT,
    farbintensität  INTEGER,
    geruch TEXT,
    geschmack TEXT,
    textur TEXT,
    konsistenz TEXT,
    anmerkung TEXT
);

-- Create the probenreihen table
CREATE TABLE probenreihen (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    proben_ids INTEGER[] NOT NULL
);

-- Create the Benutzer table
CREATE TABLE benutzer (
    id SERIAL PRIMARY KEY,
    benutzername TEXT NOT NULL,
    passwort TEXT NOT NULL,
    rolle BOOLEAN NOT NULL,
    training_id INTEGER,
    aktiv BOOLEAN NOT NULL DEFAULT false,
    last_activity TIMESTAMP,
    FOREIGN KEY (training_id) REFERENCES trainings (id)
);

-- Create the dreieckstest table
CREATE TABLE dreieckstest (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    probenreihe_id_1 INTEGER NOT NULL,
    probenreihe_id_2 INTEGER NOT NULL,
    FOREIGN KEY (probenreihe_id_1) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (probenreihe_id_2) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the konz_reihe table
CREATE TABLE konz_reihe (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    probenreihe_id INTEGER NOT NULL,
    FOREIGN KEY (probenreihe_id) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the profilprüfung table
CREATE TABLE profilprüfung (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    proben_id INTEGER NOT NULL,
    kriterien TEXT[],
    FOREIGN KEY (proben_id) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the hedonische_beurteilung table
CREATE TABLE hed_beurteilung (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    probenreihe_id INTEGER NOT NULL,
    FOREIGN KEY (probenreihe_id) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the auswahltest table
CREATE TABLE auswahltest (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    probenreihe_id INTEGER NOT NULL,
    FOREIGN KEY (probenreihe_id) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the geruchserkennung table
CREATE TABLE geruchserkennung (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    probenreihe_id INTEGER NOT NULL,
    geruch_mit_auswahl INTEGER,
    FOREIGN KEY (probenreihe_id) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the paar_vergleich table
CREATE TABLE paar_vergleich (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    probenreihe_id_1 INTEGER NOT NULL,
    probenreihe_id_2 INTEGER NOT NULL,
    FOREIGN KEY (probenreihe_id_1) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (probenreihe_id_2) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the EBP table
CREATE TABLE ebp (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    proben_id INTEGER NOT NULL,
    FOREIGN KEY (proben_id) REFERENCES proben (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Create the rangordnungstest table
CREATE TABLE rangordnungstest (
    id SERIAL PRIMARY KEY,
    aufgabenstellung_id INTEGER,
    probenreihe_id INTEGER NOT NULL,
    FOREIGN KEY (probenreihe_id) REFERENCES probenreihen (id) ON DELETE CASCADE,
    FOREIGN KEY (aufgabenstellung_id) REFERENCES aufgabenstellungen (id) ON DELETE CASCADE
);

-- Add foreign key constraints for the fragens table

INSERT INTO public.benutzer(
	benutzername, passwort, rolle, training_id)
	VALUES 
    ('Test', '123', TRUE, NULL),
    ('Student1', '123', False, NULL),
    ('Student2', '123', False, NULL),
    ('Student3', '123', False, NULL);

INSERT INTO public.proben(
	proben_nr, probenname, farbe, farbintensität , geruch, geschmack, textur, konsistenz)
	VALUES 
    (999, 'Schwarzdorn', 'Schwarz', 100, 'erdig', 'salzig', 'rau', 'fest'),
    (345, 'Mondlicht', 'Silber', 50, 'sanft', 'leicht süßlich', 'glatt', 'zart'),
    (721, 'Feuerherz', 'Rot', 80, 'intensiv', 'fruchtig', 'wärmend', 'weich'),
    (567, 'Waldesrauschen', 'Grün', 70, 'frisch', 'holzig', 'beruhigend', 'knackig'),
    (123, 'Sternenstaub', 'Gold', 60, 'zauberhaft', 'glitzernd', 'seidig', 'leicht'),
    (888, 'Eiskristall', 'Blau', 90, 'klar', 'kühlend', 'glänzend', 'spröde'),
    (432, 'Sonnenglanz', 'Gelb', 75, 'strahlend', 'frisch', 'lebhaft', 'knusprig'),
    (654, 'Nebelschwade', 'Grau', 40, 'geheimnisvoll', 'nebelig', 'hauchdünn', 'leicht'),
    (777, 'Klangwelle', 'Violett', 85, 'schwingend', 'sphärisch', 'sanft', 'glatt'),
    (222, 'Blütenregen', 'Rosa', 55, 'zart', 'blumig', 'fallend', 'leicht');

INSERT INTO public.probenreihen(
	name, proben_ids)
	VALUES 
    ('Testreihe', ARRAY[1,1]),
    ('Testreihe 2', ARRAY[7, 8, 9]),
    ('Testreihe 3', ARRAY[5, 1, 4]),
    ('Testreihe 4', ARRAY[3, 4, 5]),
    ('Testreihe 5', ARRAY[6, 7, 8]),
    ('Testreihe 6', ARRAY[9, 2]),
    ('Testreihe 7', ARRAY[1, 2]),
    ('Testreihe 8', ARRAY[3, 4]),
    ('Testreihe 9', ARRAY[5, 6]),
    ('Testreihe 10', ARRAY[7, 8]),
    ('Testreihe 11', ARRAY[9, 3]);

INSERT INTO public.prüfvarianten(
	prüfname)
	VALUES 
	('Erkennung von unterschiedlichen Geschmacksintensitäten'),
	('Erkennung von unterschiedlichen Farbintensitäten'),
	('Paarweise Vergleichsprüfung'),
	('Paarweise Vergleichsprüfung (einseitiger test)'),
	('Geruchserkennungprüfung A'),
	('Geruchserkennungprüfung B'),
	('Erkennen der 4 Grundgeschmacksarten'),
	('Erkennen von verschiedenen Salzen'),
	('Dreiecksprüfung'),
	('Erweiterte Hedonische Beurteilung'),
	('Profilprüfung');

INSERT INTO public.aufgabenstellungen(
	aufgabenstellung, aufgabentyp, prüfvarianten_id)
	VALUES 
    ('Beschreiben Sie bitte die Merkmale des Ihnen vorliegenden Prüfgutes', 'ebp',NULL),
    ('Mit diesem Test soll Ihre Fähigkeit der Erkennung verschieden starker Geschmacksintensitäten ermittelt werden. Ordnen Sie deshalb die Proben nach zunehmender Geschmacksintensität.', 'rangordnungstest', 1),
    ('Ordnen Sie die Proben nach Farbintensität. Notieren Sie die Zahlen der Proben von hell nach dunkel. ', 'rangordnungstest',2),
    ('Ihnen liegen 2 Probensätze mit jeweils zwei Prüfproben vor. Beantworten Sie bitte für jedes Probenpaar die Prüffrage und tragen Sie die zutreffende Antwort in der Spalte “Antwort” entsprechend ein.', 'paar_vergleich',3),
    ('Ihnen liegen 2 Probensätze vor.  Beantworten Sie bitte für das Probenpaar die Prüffrage und tragen Sie die zutreffende Antwort in der Spalte “Antwort” entsprechend ein.', 'paar_vergleich',4),
    ('Versuchen Sie den zu prüfenden Geruch zu erkennen und tragen Sie das Ergebnis unter "Geruchserkennung ohne Auswahlliste" ein. Beschreiben Sie den Geruch', 'geruchserkennung',5),
    ('Sie erhalten eine Liste mit Vorschlägen möglicher Aromen. Prüfen Sie nun die Aromen erneut und tragen Sie Ihr Ergebnisse in der Spalte "Geruchserkennung mit Auswahlliste" ein. ', 'geruchserkennung',6),
    ('Versuchen Sie bei den 6 Reaktionsgefäßen den Geruch zu erkennen und tragen Sie das Ergebnis unter "Geruchserkennung ohne Auswahlliste" ein. Bescreiben Sie den Geruch', 'geruchserkennung',5),
    ('Beschriften Sie Verkostungsbecher mit den untenstehenden Probennummern. Sehen Sie zusätzlichen Becher für das Referenzwasser vor. Sie erhalten 10 verschiedene wässrige Lösungen, die Saccharose (süß), Natriumchlorid (salzig), Citronensäure (sauer) und Coffein (bitter) in geringer Konzentration enthalten. Stellen Sie die Becher entsprechend der Probennummern von links nach rechts auf. Die vorgelegten Proben sind durch “Schmecken” von links nach rechts zu prüfen und in der entsprechenden Spalte durch ein Kreuz (X) zu kennzeichnen. Rückkosten ist nicht erlaubt ', 'auswahltest',7),
    ('Beschriften Sie Verkostungsbecher mit den untenstehenden Probennummern. Sie erhalten 5 verschiedene wässrige Lösungen mit den Salzen, und eine mit Zreferenzwasser.', 'auswahltest',8),
    ('Ihnen liegen zwei Probensätze mit jeweils drei codierten Proben vor. In jedem Probensatz sind zwei Proben identisch und eine Probe abweichend. Verkosten Sie die Proben bitte in der vorgegebenen Reihenfolge (Prüfproben von links nach rechts) und tragen Sie jeweils die abweichende Probe ein.Rückkosten ist erlaubt. Wenn Sie den Unterschied nicht sicher erkennen, müssen Sie raten.', 'dreieckstest',9),
    ('Bitte beurteilen Sie die Probe nach Ihrem Geschmacksempfinden und kreuzen Sie die zutreffende Aussage an.', 'hed_beurteilung',10),
    ('Beurteilen Sie die Proben einzeln nach den nachfolgend aufgelisten Kriterien. Ordnen Sie jeweils einen Intensitätswert zu. Konzentrieren Sie sich dabei jeweils nur auf die Wahrnehmung des angeführten Parameters. Tragen Sie die Proben auf der Linienskala von 0 bis 10 ein. ', 'profilprüfung',11),
    ('Probieren Sie die aufgelisteten Proben in der angegebnen Reihenfolge und kennzeichnen Sie jede getestete Probe mit einem Symbol in der Legende. ', 'konz_reihe',NULL)        


            ''')
#TODO: Aufgabenstellung: Konzentrationsreihen, Verschlussverkostung

conn.commit()
cur.close()
conn.close()

"""
-------------------
--- AUSSORTIERT ---
-------------------

-- Create the Fragen table
CREATE TABLE fragen (
    id SERIAL PRIMARY KEY,
    fragen_typ VARCHAR(255) NOT NULL,
    fragen_id INTEGER NOT NULL
);

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
"""