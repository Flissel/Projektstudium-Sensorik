from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FieldList, FormField, HiddenField
from wtforms.validators import DataRequired
from model import Trainings, Aufgabenstellungen, Probenreihen, Proben


class ModifyForm(FlaskForm):
    question_type = SelectField("Fragentyp", choices=[
                ('ebp', 'Einfach beschreibende Prüfung'), 
                ('rangordnungstest', 'Rangordnungstest'), 
                ('auswahltest', 'Auswahltest'),
                ('dreieckstest', 'Dreieckstest'),
                ('geruchserkennung', 'Geruchserkennung'),
                ('hed_beurteilung', 'Hedonische Beurteilung'),
                ('konz_reihe', 'Konzentrationsreihe'),
                ('paar_vergleich', 'Paarweise Vergleichstest'),
                ('profilprüfung', 'Profilprüfung')
            ]
        , default="ebp")
    add = SubmitField("Hinzufügen")
    
class CreateProfilprüfung(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    proben_id = SelectField('Probe', choices=[])
    kriterien = FieldList(StringField("Kriterium"))

    def __init__(self, *args, **kwargs):
        super(CreateProfilprüfung, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="profilprüfung").all()]
        self.proben_id.choices = [(p.id, p.probenname) for p in Proben.query.all()]

class CreatePaar_vergleich(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id_1 = SelectField('1. Probenreihe', choices=[])
    probenreihe_id_2 = SelectField('2. Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreatePaar_vergleich, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="paar_vergleich").all()]
        self.probenreihe_id_1.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.probenreihe_id_2.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class CreateKonz_reihe(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateKonz_reihe, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="konz_reihe").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class CreateHed_beurteilung(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateHed_beurteilung, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="hed_beurteilung").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class CreateGeruchserkennung(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    proben_id = SelectField('Probe', choices=[])
    # Eventuell dem Professor die Möglichkeit geben die Auswahl für jede Frage selbst zu definieren.
    # Momentan ist Auswahlliste in "geruchsauswahl" Tabelle gespeichert
    # Eventuell Möglichkeit einräumen diese Liste zu verändern

    def __init__(self, *args, **kwargs):
        super(CreateGeruchserkennung, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="geruchserkennung").all()]
        self.proben_id.choices = [(p.id, p.probenname) for p in Proben.query.all()]

class CreateDreieckstest(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])
    lösung = SelectField('Lösungsprobe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateDreieckstest, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="dreieckstest").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.lösung.choices = [(p.id, p.probenname) for p in Proben.query.all()]

class CreateAuswahltest(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateAuswahltest, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="auswahltest").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class CreateRangordnungstestForm(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateRangordnungstestForm, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="rangordnungstest").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class CreateEbpForm(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    proben_id = SelectField('Proben ID', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateEbpForm, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="ebp").all()]
        self.proben_id.choices = [(p.id, p.probenname) for p in Proben.query.all()]

class CreateTrainingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    question_types = FieldList(FormField(ModifyForm), min_entries=1)
    ebp_questions = FieldList(FormField(CreateEbpForm))
    rangordnungstest_questions = FieldList(FormField(CreateRangordnungstestForm))
    auswahltest_questions = FieldList(FormField(CreateAuswahltest))
    dreieckstest_questions = FieldList(FormField(CreateDreieckstest))
    geruchserkennung_questions = FieldList(FormField(CreateGeruchserkennung))
    hed_beurteilung_questions = FieldList(FormField(CreateHed_beurteilung))
    konz_reihe_questions = FieldList(FormField(CreateKonz_reihe))
    paar_vergelich_questions = FieldList(FormField(CreatePaar_vergleich))
    profilprüfung_questions = FieldList(FormField(CreateProfilprüfung))
    submit = SubmitField('Trainings erstellen')

class TrainingsViewForm(FlaskForm):
    trainings = SelectField('Trainings', choices=[])
    delete = SubmitField('Löschen')

    def __init__(self, *args, **kwargs):
        super(TrainingsViewForm, self).__init__(*args, **kwargs)
        self.trainings.choices = [(t.id, t.name) for t in Trainings.query.all()]