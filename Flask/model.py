from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY

db = SQLAlchemy()

"""
Allgemeine Tabllen (benutzer, proben, trainings etc.)
"""

class Aufgabenstellungen(db.Model):
    """
    Table for Aufgabenstellungen.
    """
    __tablename__ = 'aufgabenstellungen'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aufgabenstellung = db.Column(db.Text, nullable=False)
    aufgabentyp = db.Column(db.Text, nullable=False)
    prüfvarianten_id = db.Column(db.Integer, db.ForeignKey('prüfvarianten.id'))


class Prüfvarianten(db.Model):
    """
    Table for Prüfvarianten.
    """
    __tablename__ = 'prüfvarianten'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prüfname = db.Column(db.Text, nullable=False)


class Trainings(db.Model):
    """
    Table for Trainings.
    """
    __tablename__ = 'trainings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    fragen_ids = db.Column(ARRAY(db.INTEGER))
    fragen_typen = db.Column(ARRAY(db.TEXT))


class Proben(db.Model):
    """
    Table for Proben.
    """
    __tablename__ = 'proben'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    proben_nr = db.Column(db.Integer, unique=True, nullable=False)
    probenname = db.Column(db.String(255), nullable=False)
    farbe = db.Column(db.Text)
    farbintensität = db.Column(db.Integer)
    geruch = db.Column(db.Text)
    geschmack = db.Column(db.Text)
    textur = db.Column(db.Text)
    konsistenz = db.Column(db.Text)
    anmerkung = db.Column(db.Text)


class Probenreihen(db.Model):
    """
    Table for Probenreihen.
    """
    __tablename__ = 'probenreihen'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text)
    proben_ids = db.Column(ARRAY(db.Integer, db.ForeignKey('proben.id')))


class Benutzer(db.Model):
    """
    Table for Benutzer.
    """
    __tablename__ = 'benutzer'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    benutzername = db.Column(db.Text, nullable=False)
    passwort = db.Column(db.Text, nullable=False)
    rolle = db.Column(db.Boolean, nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id'))
    aktiv = db.Column(db.Boolean, nullable=False)
    last_activity = db.Column(db.TIMESTAMP)


"""
Fragetyp Tabellen (ebp, rangordnungstest, Auswahltest etc.)
"""


class Konz_reihe(db.Model):
    """
    Table for Konz_reihe.
    """
    __tablename__ = "konz_reihe"

    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))


class Profilprüfung(db.Model):
    """
    Table for Profilprüfung.
    """
    __tablename__ = "profilprüfung"

    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    proben_id = db.Column(db.Integer, db.ForeignKey('proben.id'))
    kriterien = db.Column(ARRAY(db.Text))


class Hed_beurteilung(db.Model):
    """
    Table for Hed_beurteilung.
    """
    __tablename__ = "hed_beurteilung"

    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))


class Auswahltest(db.Model):
    """
    Table for Auswahltest.
    """
    __tablename__ = "auswahltest"

    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))


class Geruchserkennung(db.Model):
    """
    Table for Geruchserkennung.
    """
    __tablename__ = "geruchserkennung"

    id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))
    geruch_mit_auswahl = db.Column(db.Text)


class Paar_vergleich(db.Model):
    """
    Table for Paar_vergleich.
    """
    __tablename__ = 'paar_vergleich'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id_1 = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))
    probenreihe_id_2 = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))


class Ebp(db.Model):
    """
    Table for Ebp.
    """
    __tablename__ = 'ebp'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    proben_id = db.Column(db.Integer, db.ForeignKey('proben.id'))


class Rangordnungstest(db.Model):
    """
    Table for Rangordnungstest.
    """
    __tablename__ = 'rangordnungstest'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))


class Dreieckstest(db.Model):
    """
    Table for Dreieckstest.
    """
    __tablename__ = 'dreieckstest'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    aufgabenstellung_id = db.Column(db.Integer, db.ForeignKey('aufgabenstellungen.id'))
    probenreihe_id_1 = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))
    probenreihe_id_2 = db.Column(db.Integer, db.ForeignKey('probenreihen.id'))
