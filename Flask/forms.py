from flask_wtf import FlaskForm
from flask import request, session
from wtforms import StringField, IntegerField, SubmitField, SelectField, FieldList, FormField, HiddenField
from wtforms.validators import DataRequired
from model import Trainings, Aufgabenstellungen, Probenreihen, Proben, Benutzer,Paar_vergleich, Probenreihen


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
    lösung_1 = SelectField('1. Lösungsprobe', choices=[])
    lösung_2 = SelectField('2. Lösungsprobe', choices=[])
    
    def __init__(self, *args, **kwargs):
        super(CreatePaar_vergleich, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="paar_vergleich").all()]
        self.probenreihe_id_1.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.probenreihe_id_2.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.lösung_1.choices = [(p.id, p.probenname) for p in Proben.query.all()]
        self.lösung_2.choices = [(p.id, p.probenname) for p in Proben.query.all()]

class CreateKonz_reihe(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])

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
    probenreihe_id_1 = SelectField('Probenreihe 1', choices=[])
    probenreihe_id_2 = SelectField('Probenreihe 2', choices=[])
    lösung_1 = SelectField('Lösungsprobe 1', choices=[])
    lösung_2 = SelectField('Lösungsprobe 2', choices=[])


    def __init__(self, *args, **kwargs):
        super(CreateDreieckstest, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="dreieckstest").all()]
        self.probenreihe_id_1.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.probenreihe_id_2.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.lösung_1.choices = [(p.id, p.probenname) for p in Proben.query.all()]
        self.lösung_2.choices = [(p.id, p.probenname) for p in Proben.query.all()]


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
    question_types = question_type = SelectField("Fragentyp", choices=[
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
    ebp_questions = FieldList(FormField(CreateEbpForm))
    rangordnungstest_questions = FieldList(FormField(CreateRangordnungstestForm))
    auswahltest_questions = FieldList(FormField(CreateAuswahltest))
    dreieckstest_questions = FieldList(FormField(CreateDreieckstest))
    geruchserkennung_questions = FieldList(FormField(CreateGeruchserkennung))
    hed_beurteilung_questions = FieldList(FormField(CreateHed_beurteilung))
    konz_reihe_questions = FieldList(FormField(CreateKonz_reihe))
    paar_vergleich_questions = FieldList(FormField(CreatePaar_vergleich))
    profilprüfung_questions = FieldList(FormField(CreateProfilprüfung))
    add_question = SubmitField('Frage hinzufügen')
    remove_ebp_question = FieldList(FormField(SubmitField('Frage entfernen')))
    remove_rangordnungstest_question = FieldList(FormField(SubmitField('Frage entfernen')))
    remove_auswahltest_question = FieldList(FormField(SubmitField('Frage entfernen')))
    remove_dreieckstest_question = FieldList(FormField(SubmitField('Frage entfernen')))
    remove_geruchserkennung_question = FieldList(FormField(SubmitField('Frage entfernen')))
    remove_hed_beurteilung_question = FieldList(FormField(SubmitField('Frage entfernen')))
    remove_konz_reihe_question = FieldList(FormField(SubmitField('Frage entfernen')))
    remove_profilprüfung_question = FieldList(FormField(SubmitField('Frage entfernen')))
    create_training = SubmitField('Trainings erstellen')
    

class TrainingsViewForm(FlaskForm):
    trainings = SelectField('Trainings', choices=[])
    delete = SubmitField('Löschen')

    def __init__(self, *args, **kwargs):
        super(TrainingsViewForm, self).__init__(*args, **kwargs)
        self.trainings.choices = [(t.id, t.name) for t in Trainings.query.all()]








###################################
#---View Forms for the students---#
###################################

class ViewProfilprüfung(FlaskForm):
    skalenwerte = FieldList(IntegerField('Skalenwert'))

class ViewPaar_vergleich(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id_1 = SelectField('1. Probenreihe', choices=[])
    probenreihe_id_2 = SelectField('2. Probenreihe', choices=[])
    lösung_1 = SelectField('1. Lösungsprobe', choices=[])
    lösung_2 = SelectField('2. Lösungsprobe', choices=[])

    proben_id_1 = SelectField('Der geschmack welcher Probe ist stärker ausgeprägt ?', choices=[])
    proben_id_2 = SelectField('Der geschmack welcher Probe ist stärker ausgeprägt ?', choices=[])
    proben_id_3 = SelectField('Der Geschmack welcher Probe entspricht eher Ihren Erwartungen an das Produkt?', choices=[])

    
    def __init__(self, *args, **kwargs):
        super(ViewPaar_vergleich, self).__init__(*args, **kwargs)
        username = session['username']
        question_index = session['question_index']
        user = Benutzer.query.filter_by(benutzername=username).first()
        training = Trainings.query.get(user.training_id)
        question = training.fragen_ids[question_index]

        self.proben_id_1.choices = [(Proben.query.get(p).id, Proben.query.get(p).probenname) for p in Probenreihen.query.get(Paar_vergleich.query.get(question).probenreihe_id_1).proben_ids]
        self.proben_id_2.choices = [(Proben.query.get(p).id, Proben.query.get(p).probenname) for p in Probenreihen.query.get(Paar_vergleich.query.get(question).probenreihe_id_2).proben_ids]
        self.proben_id_3.choices = self.proben_id_1.choices + self.proben_id_2.choices



class Konz_reihe(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateKonz_reihe, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="konz_reihe").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class Hed_beurteilung(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateHed_beurteilung, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="hed_beurteilung").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class Geruchserkennung(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    proben_id = SelectField('Probe', choices=[])
    # Eventuell dem Professor die Möglichkeit geben die Auswahl für jede Frage selbst zu definieren.
    # Momentan ist Auswahlliste in "geruchsauswahl" Tabelle gespeichert
    # Eventuell Möglichkeit einräumen diese Liste zu verändern

    def __init__(self, *args, **kwargs):
        super(CreateGeruchserkennung, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="geruchserkennung").all()]
        self.proben_id.choices = [(p.id, p.probenname) for p in Proben.query.all()]

class Dreieckstest(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id_1 = SelectField('Probenreihe 1', choices=[])
    probenreihe_id_2 = SelectField('Probenreihe 2', choices=[])
    lösung_1 = SelectField('Lösungsprobe 1', choices=[])
    lösung_2 = SelectField('Lösungsprobe 2', choices=[])


    def __init__(self, *args, **kwargs):
        super(CreateDreieckstest, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="dreieckstest").all()]
        self.probenreihe_id_1.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.probenreihe_id_2.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.lösung_1.choices = [(p.id, p.probenname) for p in Proben.query.all()]
        self.lösung_2.choices = [(p.id, p.probenname) for p in Proben.query.all()]


class Auswahltest(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateAuswahltest, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="auswahltest").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class RangordnungstestForm(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateRangordnungstestForm, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="rangordnungstest").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class EbpForm(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    proben_id = SelectField('Proben ID', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateEbpForm, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="ebp").all()]
        self.proben_id.choices = [(p.id, p.probenname) for p in Proben.query.all()]