from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Proben(db.Model):
    __tablename__ = 'proben'
    id = db.Column(db.Integer, primary_key=True)
    proben_nr = db.Column(db.Integer, unique=True, nullable=False)
    probenname = db.Column(db.String(255), nullable=False)
    aussehen_farbe = db.Column(db.Text, nullable=True)
    geruch = db.Column(db.Text, nullable=True)
    geschmack = db.Column(db.Text, nullable=True)
    textur = db.Column(db.Text, nullable=True)
    konsistenz = db.Column(db.Text, nullable=True)

class EBP(db.Model):
    __tablename__ = 'ebp'
    id = db.Column(db.Integer, primary_key=True)
    proben_id = db.Column(db.Integer, db.ForeignKey('proben.id', ondelete='CASCADE'))
    aussehen_farbe = db.Column(db.Text, nullable=True)
    geruch = db.Column(db.Text, nullable=True)
    geschmack = db.Column(db.Text, nullable=True)
    textur = db.Column(db.Text, nullable=True)
    konsistenz = db.Column(db.Text, nullable=True)

    probe = db.relationship('Proben', backref=db.backref('ebp', lazy='dynamic'))

class Rangordnungstest(db.Model):
    __tablename__ = 'rangordnungstest'
    id = db.Column(db.Integer, primary_key=True)
    proben_id_1 = db.Column(db.Integer, db.ForeignKey('proben.id', ondelete='CASCADE'))
    proben_id_2 = db.Column(db.Integer, db.ForeignKey('proben.id', ondelete='CASCADE'))
    proben_id_3 = db.Column(db.Integer, db.ForeignKey('proben.id', ondelete='CASCADE'))
    proben_id_4 = db.Column(db.Integer, db.ForeignKey('proben.id', ondelete='CASCADE'))
    proben_id_5 = db.Column(db.Integer, db.ForeignKey('proben.id', ondelete='CASCADE'))

    probe_1 = db.relationship('Proben', foreign_keys=[proben_id_1], backref=db.backref('rangordnungstest_1', lazy='dynamic'))
    probe_2 = db.relationship('Proben', foreign_keys=[proben_id_2], backref=db.backref('rangordnungstest_2', lazy='dynamic'))
    probe_3 = db.relationship('Proben', foreign_keys=[proben_id_3], backref=db.backref('rangordnungstest_3', lazy='dynamic'))
    probe_4 = db.relationship('Proben', foreign_keys=[proben_id_4], backref=db.backref('rangordnungstest_4', lazy='dynamic'))
    probe_5 = db.relationship('Proben', foreign_keys=[proben_id_5], backref=db.backref('rangordnungstest_5', lazy='dynamic'))


class Questions(db.Model):
    __tablename__ = 'fragen'
    id = db.Column(db.Integer, primary_key=True)
    fragen_typ = db.Column(db.String(255), nullable=False)
    fragen_id = db.Column(db.Integer, nullable=False)

class Trainings(db.Model):
    __tablename__ = 'trainings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    question_id_1 = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))
    question_id_2 = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))
    question_id_3 = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))
    question_id_4 = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))
    question_id_5 = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))
    question_id_6 = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))
    question_id_7 = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))
    question_id_8 = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))
    question_id_9 = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))
    question_id_10 = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'))

class Benutzer(db.Model):
    __tablename__ = 'benutzer'
    id = db.Column(db.Integer, primary_key=True)
    benutzername = db.Column(db.String(255), nullable=False)
    passwort = db.Column(db.String(255), nullable=False)
    rolle = db.Column(db.Boolean, nullable=False)
    training_id = db.Column(db.Integer, db.ForeignKey('trainings.id', ondelete='CASCADE'))
    training = db.relationship('Trainings', backref=db.backref('benutzer', lazy='dynamic'))

