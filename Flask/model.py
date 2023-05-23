from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()

"""
Allgemeine Tabllen (benutzer, proben, trainings etc.)
"""

class Fragen(db.Model):
    __tablename__ = 'fragen'

    id = db.Column(db.Integer, primary_key=True)
    fragen_typ = db.Column(db.String(255), nullable=False)
    fragen_id = db.Column(db.Integer, nullable=False)

class Aufgabenstellungen(db.Model):
    __tablename__ = 'aufgabenstellungen'

    id = db.Column(db.Integer, primary_key=True)
    aufgabenstellung = db.Column(db.Text, nullable=False)
    aufgabentyp = db.Column(db.Text, nullable=False)
    prüfvarianten_id = db.Column(db.Integer, db.ForeignKey('prüfvarianten', ondelete='CASCADE'))

class Trainings(db.Model):
    __tablename__ = 'trainings'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    reference = db.Column(db.Text)

class Proben(db.Model):
    __tablename__ = 'proben'

    id = db.Column(db.Integer, primary_key=True)
    proben_nr = db.Column(db.Integer, unique=True, nullable=False)
    probenname = db.Column(db.String(255), nullable=False)
    farbe = db.Column(db.Text)
    farbintensität = db.Column(db.Integer)
    geruch = db.Column(db.Text)
    geschmack = db.Column(db.Text)
    textur = db.Column(db.Text)
    konsistenz = db.Column(db.Text)

class Probenreihen(db.Model):

    __tablename__ = 'probenreihen'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    proben_id = db.Column(db.Integer, db.ForeignKey('proben.id', ondelete='CASCADE'))

class Benutzer(db.Model):
    __tablename__ = 'benutzer'

    id = db.Column(db.Integer, primary_key=True)
    benutzername = db.Column(db.Text, nullable=False)
    passwort = db.Column(db.Text, nullable=False)
    rolle = db.Column(db.Boolean, nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id', ondelete='CASCADE'))


"""
Fragetyp Tabellen (ebp, rangordnungstest, Auswahltest etc.)
"""

class Konz_reihe(db.Model):
    __tablename__ = "konz_reihe"

    id = db.Column(db.Integer, primary_key=True, index=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))
    antworten = db.Column(ARRAY(db.Text))

class Profilprüfung(db.Model):
    __tablename__ = "profilprüfung"

    id = db.Column(db.Integer, primary_key=True, index=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    proben_id = db.Column(db.Integer, db.ForeignKey('proben.id'))
    kriterien = db.Column(ARRAY(db.Text))
    bewertungen = db.Column(ARRAY(db.Integer))

class Hed_beurteilung(db.Model):
    __tablename__ = "hed_beurteilung"

    id = db.Column(db.Integer, primary_key=True, index=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))
    beurteilung = db.Column(ARRAY(db.Text))
    anmerkung = db.Column(ARRAY(db.Text))

class Auswahltest(db.Model):
    __tablename__ = "auswahltest"

    id = db.Column(db.Integer, primary_key=True, index=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id= db.Column(db.Integer, db.ForeignKey('probenreihen.id'))
    bemerkungen = db.Column(ARRAY(db.Text))

class Geruchserkennung(db.Model):
    __tablename__ = "geruchserkennung"

    id = db.Column(db.Integer, primary_key=True, index=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    proben_id = db.Column(db.Integer, db.ForeignKey('proben.id'))
    geruch_ohne_auswahl = db.Column(db.Text)
    geruch_mit_auswahl = db.Column(db.Text)
    bemerkung = db.Column(db.Text)
    
class Paar_vergleich(db.Model):
    __tablename__ = 'paar_vergleich'
    id = db.Column(db.Integer, primary_key=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('proben.id'))
    lösung = db.Column(db.Integer)
    bemerkung = db.Column(db.Text)

class Ebp(db.Model):
    __tablename__ = 'ebp'
    id = db.Column(db.Integer, primary_key=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    proben_id = db.Column(db.Integer, db.ForeignKey('proben.id'))
    aussehen_farbe = db.Column(db.Text)
    geruch = db.Column(db.Text)
    geschmack = db.Column(db.Text)
    textur = db.Column(db.Text)
    konsistenz = db.Column(db.Text)

class Rangordnungstest(db.Model):
    __tablename__ = 'rangordnungstest'
    id = db.Column(db.Integer, primary_key=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))
    rang_1_proben_id = db.Column(db.Integer)
    rang_2_proben_id = db.Column(db.Integer)
    rang_3_proben_id = db.Column(db.Integer)
    rang_4_proben_id = db.Column(db.Integer)
    rang_5_proben_id = db.Column(db.Integer)

class Dreieckstest(db.Model):
    __tablename__ = 'dreieckstest'
    id = db.Column(db.Integer, primary_key=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))
    lösung = db.Column(db.Integer, db.ForeignKey('proben.id'))
