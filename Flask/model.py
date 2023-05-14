from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

"""
Allgemeine Tabllen (benutzer, proben, trainings etc.)
"""

class Fragen(db.model):
    __tablename__ = 'fragen'

    id = db.Column(db.Integer, primary_key=True)
    fragen_typ = db.Column(db.String(255), nullable=False)
    fragen_id = db.Column(db.Integer, nullable=False)

class Aufgabenstellungen(db.model):
    __tablename__ = 'aufgabenstellungen'

    id = db.Column(db.Integer, primary_key=True)
    db.Text = db.Column(db.Text, nullable=False)
    aufgabentyp = db.Column(db.Text, nullable=False)

class Trainings(db.model):
    __tablename__ = 'trainings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    fragen_id_1 = db.Column(db.Integer, db.ForeignKey('fragen.id', ondelete='CASCADE'))
    fragen_id_2 = db.Column(db.Integer, db.ForeignKey('fragen.id', ondelete='CASCADE'))
    # ... and so on for the rest of the fragen_ids

class Proben(db.model):
    __tablename__ = 'proben'

    id = db.Column(db.Integer, primary_key=True)
    proben_nr = db.Column(db.Integer, unique=True, nullable=False)
    probenname = db.Column(db.String(255), nullable=False)
    farbe = db.Column(db.Text)
    farbintensität = db.Column(db.Integer)
    geruch = db.Column(db.Text)
    geschmack = db.Column(db.Text)
    db.Textur = db.Column(db.Text)
    konsistenz = db.Column(db.Text)

class Probenreihen(db.model):

    __tablename__ = 'probenreihen'

    id = db.Column(db.Integer, primary_key=True)
    proben_id_1 = db.Column(db.Integer, db.ForeignKey('proben.id', ondelete='CASCADE'))
    # ... and so on for the rest of the proben_ids

class Benutzer(db.model):
    __tablename__ = 'benutzer'

    id = db.Column(db.Integer, primary_key=True)
    benutzername = db.Column(db.Text, nullable=False)
    passwort = db.Column(db.Text, nullable=False)
    rolle = db.Column(db.Boolean, nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id', ondelete='CASCADE'))


"""
Fragetyp Tabellen (ebp, rangordnungstest, Auswahltest etc.)
"""

class KonzReihe(db.model):
    __tablename__ = "konz_reihe"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))
    probe_1_antwort = db.Column(db.String)
    probe_2_antwort = db.Column(db.String)
    probe_3_antwort = db.Column(db.String)
    probe_4_antwort = db.Column(db.String)
    probe_5_antwort = db.Column(db.String)
    probe_6_antwort = db.Column(db.String)
    probe_7_antwort = db.Column(db.String)
    probe_8_antwort = db.Column(db.String)
    probe_9_antwort = db.Column(db.String)
    probe_10_antwort = db.Column(db.String)

class ProfilPrüfung(db.model):
    __tablename__ = "profilprüfung"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    proben_id = db.Column(db.Integer, db.ForeignKey('proben.id'))
    kriterium_1 = db.Column(db.String)
    kriterium_2 = db.Column(db.String)
    kriterium_3 = db.Column(db.String)
    kriterium_4 = db.Column(db.String)
    kriterium_5 = db.Column(db.String)
    kriterium_6 = db.Column(db.String)
    kriterium_7 = db.Column(db.String)
    kriterium_8 = db.Column(db.String)
    kriterium_9 = db.Column(db.String)
    skalenbewertung_1 = db.Column(db.Integer)
    skalenbewertung_2 = db.Column(db.Integer)
    skalenbewertung_3 = db.Column(db.Integer)
    skalenbewertung_4 = db.Column(db.Integer)
    skalenbewertung_5 = db.Column(db.Integer)
    skalenbewertung_6 = db.Column(db.Integer)
    skalenbewertung_7 = db.Column(db.Integer)
    skalenbewertung_8 = db.Column(db.Integer)
    skalenbewertung_9 = db.Column(db.Integer)

class HedBeurteilung(db.model):
    __tablename__ = "hed_beurteilung"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    proben_id = db.Column(db.Integer, db.ForeignKey('proben.id'))
    beurteilung = db.Column(db.String)
    anmerkung = db.Column(db.String)

class Auswahltest(db.model):
    __tablename__ = "auswahltest"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    prüfvariante = db.Column(db.String)
    proben_id_1 = db.Column(db.Integer, db.ForeignKey('proben.id'))
    proben_id_2 = db.Column(db.Integer, db.ForeignKey('proben.id'))
    proben_id_3 = db.Column(db.Integer, db.ForeignKey('proben.id'))
    proben_id_4 = db.Column(db.Integer, db.ForeignKey('proben.id'))
    proben_id_5 = db.Column(db.Integer, db.ForeignKey('proben.id'))
    proben_id_6 = db.Column(db.Integer, db.ForeignKey('proben.id'))
    bemerkung_1 = db.Column(db.String)
    bemerkung_2 = db.Column(db.String)
    bemerkung_3 = db.Column(db.String)
    bemerkung_4 = db.Column(db.String)
    bemerkung_5 = db.Column(db.String)
    bemerkung_6 = db.Column(db.String)

class Geruchserkennung(db.model):
    __tablename__ = "geruchserkennung"

    id = db.Column(db.Integer, primary_key=True, index=True)
    title_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probe_id = db.Column(db.Integer, db.ForeignKey('proben.id'))
    geruch = db.Column(db.String)
    intensität = db.Column(db.Integer)
    anmerkung = db.Column(db.String)
    
class PaarVergleich(db.model):
    __tablename__ = 'paar_vergleich'
    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    prüfvariante = db.Column(db.String)
    proben_id_1 = db.Column(db.Integer, db.ForeignKey('proben.id'))
    proben_id_2 = db.Column(db.Integer, db.ForeignKey('proben.id'))
    proben_auswahl_id = db.Column(db.String)
    bemerkung = db.Column(db.String)

class Ebp(db.model):
    __tablename__ = 'ebp'
    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    prüfvariante = db.Column(db.String)
    proben_id = db.Column(db.Integer, db.ForeignKey('proben.id'))
    aussehen_farbe = db.Column(db.String)
    geruch = db.Column(db.String)
    geschmack = db.Column(db.String)
    textur = db.Column(db.String)
    konsistenz = db.Column(db.String)

class Rangordnungstest(db.model):
    __tablename__ = 'rangordnungstest'
    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    prüfvariante = db.Column(db.String)
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))
    rang_1_proben_id = db.Column(db.Integer)
    rang_2_proben_id = db.Column(db.Integer)
    rang_3_proben_id = db.Column(db.Integer)
    rang_4_proben_id = db.Column(db.Integer)
    rang_5_proben_id = db.Column(db.Integer)

class Dreieckstest(Base):
    __tablename__ = 'dreieckstest'
    id = db.Column(db.Integer, primary_key=True)
    title_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    prüfvariante = db.Column(db.String)
    proben_id_1 = db.Column(db.Integer, db.ForeignKey('proben.id'))
    proben_id_2 = db.Column(db.Integer, db.ForeignKey('proben.id'))
    abweichende_probe = db.Column(db.Integer)
