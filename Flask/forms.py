from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FieldList, FormField, HiddenField, BooleanField
from wtforms.validators import DataRequired
from model import Trainings, Aufgabenstellungen, Probenreihen, Proben


class CreateProfilprüfung(FlaskForm):
    """
    Form for creating Profilprüfung task.
    """
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    proben_id = SelectField('Probe', choices=[])
    kriterien = FieldList(StringField("Kriterium"))

    def __init__(self, *args, **kwargs):
        super(CreateProfilprüfung, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(
            aufgabentyp="profilprüfung").all()]
        self.proben_id.choices = [(p.id, p.probenname) for p in Proben.query.all()]


class CreatePaar_vergleich(FlaskForm):
    """
    Form for creating Paar_vergleich task.
    """
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id_1 = SelectField('1. Probenreihe', choices=[])
    probenreihe_id_2 = SelectField('2. Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreatePaar_vergleich, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(
            aufgabentyp="paar_vergleich").all()]
        self.probenreihe_id_1.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.probenreihe_id_2.choices = [(p.id, p.name) for p in Probenreihen.query.all()]


class CreateKonz_reihe(FlaskForm):
    """
    Form for creating Konz_reihe task.
    """
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateKonz_reihe, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(
            aufgabentyp="konz_reihe").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]


class CreateHed_beurteilung(FlaskForm):
    """
    Form for creating Hed_beurteilung task.
    """
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateHed_beurteilung, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(
            aufgabentyp="hed_beurteilung").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]


class CreateGeruchserkennung(FlaskForm):
    """
    Form for creating Geruchserkennung task.
    """
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])
    geruchsauswahl = SelectField('Geruchsauswahl (Irrelevant bei Test ohne Auswahlliste)', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateGeruchserkennung, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(
            aufgabentyp="geruchserkennung").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.geruchsauswahl.choices = [(p.id, p.name) for p in Probenreihen.query.all()]


class CreateDreieckstest(FlaskForm):
    """
    Form for creating Dreieckstest task.
    """
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id_1 = SelectField('Probenreihe 1', choices=[])
    probenreihe_id_2 = SelectField('Probenreihe 2', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateDreieckstest, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(
            aufgabentyp="dreieckstest").all()]
        self.probenreihe_id_1.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.probenreihe_id_2.choices = [(p.id, p.name) for p in Probenreihen.query.all()]


class CreateAuswahltest(FlaskForm):
    """
    Form for creating Auswahltest task.
    """
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateAuswahltest, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(
            aufgabentyp="auswahltest").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]


class CreateRangordnungstestForm(FlaskForm):
    """
    Form for creating Rangordnungstest task.
    """
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateRangordnungstestForm, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(
            aufgabentyp="rangordnungstest").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]


class CreateEbpForm(FlaskForm):
    """
    Form for creating Ebp task.
    """
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    proben_id = SelectField('Proben ID', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateEbpForm, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(
            aufgabentyp="ebp").all()]
        self.proben_id.choices = [(p.id, p.probenname) for p in Proben.query.all()]


class CreateTrainingForm(FlaskForm):
    """
    Form for creating Training.
    """
    name = StringField('Name', validators=[DataRequired()])
    question_types = SelectField("Fragentyp", choices=[
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
    remove_ebp_question = FieldList(SubmitField('Frage entfernen'))
    remove_rangordnungstest_question = FieldList(SubmitField('Frage entfernen'))
    remove_auswahltest_question = FieldList(SubmitField('Frage entfernen'))
    remove_dreieckstest_question = FieldList(SubmitField('Frage entfernen'))
    remove_geruchserkennung_question = FieldList(SubmitField('Frage entfernen'))
    remove_hed_beurteilung_question = FieldList(SubmitField('Frage entfernen'))
    remove_konz_reihe_question = FieldList(SubmitField('Frage entfernen'))
    remove_profilprüfung_question = FieldList(SubmitField('Frage entfernen'))
    create_training = SubmitField('Trainings erstellen')


class TrainingsViewForm(FlaskForm):
    """
    Form for viewing Trainings.
    """
    trainings = SelectField('Trainings', choices=[])
    delete = SubmitField('Löschen')

    def __init__(self, *args, **kwargs):
        super(TrainingsViewForm, self).__init__(*args, **kwargs)
        self.trainings.choices = [(t.id, t.name) for t in Trainings.query.all()]


class ViewProfilprüfung(FlaskForm):
    """
    Form for viewing Profilprüfung task.
    """
    aufgabenstellung = StringField('')
    probe = StringField('')
    kriterien = FieldList(StringField(''))
    skalenwerte = FieldList(SelectField('', choices=[('0', '0 (zu schwach)'), ('1', '1'), ('2', '2'), ('3', '3'),
                                                     ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
                                                     ('9', '9'), ('10', '10 (zu stark)')]))


class ViewPaar_vergleich(FlaskForm):
    """
    Form for viewing Paar_vergleich task.
    """
    aufgabenstellung = StringField('')
    proben_1 = FieldList(StringField(''))
    proben_2 = FieldList(StringField(''))
    ausgeprägte_probe_1 = SelectField('Der Geschmack welcher Probe ist stärker ausgeprägt ?', choices=[])
    ausgeprägte_probe_2 = SelectField('Der Geschmack welcher Probe ist stärker ausgeprägt ?', choices=[])
    bemerkung_1 = StringField('Bemerkung: ')
    bemerkung_2 = StringField('Bemerkung: ')
    erwartung_probe = SelectField('Der Geschmack welcher Probe entspricht eher Ihren Erwartungen an das Produkt ?',
                                  choices=[])


class ViewKonz_reihe(FlaskForm):
    """
    Form for viewing Konz_reihe task.
    """
    aufgabenstellung = StringField('')
    proben = FieldList(StringField(''))
    konzentration = FieldList(SelectField('Konzentration: ',
                                          choices=[("0", "0"), ("?", "?"), ("X", "X"), ("XX", "XX"), ("XXX", "XXX")]))
    bemerkungen = FieldList(StringField('Anmerkung: '))


class ViewHed_beurteilung(FlaskForm):
    """
    Form for viewing Hed_beurteilung task.
    """
    aufgabenstellung = StringField('')
    proben = FieldList(StringField(''))
    einordnungen = FieldList(SelectField('Einordnung: ', choices=[
        ("mag ich besonders gern", "Mag ich besonders gern"),
        ("mag ich sehr gern", "Mag ich sehr gern"),
        ("mag ich gern", "Mag ich gern"),
        ("mag ich etwas", "Mag ich etwas"),
        ("weder dafür noch dagegen", "Weder dafür noch dagegen"),
        ("etwas dagegen", "Etwas dagegen"),
        ("mag ich wenig", "Mag ich wenig"),
        ("mag ich sehr wenig", "Mag ich sehr wenig"),
        ("mag ich überhaupt nicht", "Mag ich überhaupt nicht"),
    ]))
    bemerkungen = FieldList(StringField('Anmerkung: '))


class ViewGeruchserkennung(FlaskForm):
    """
    Form for viewing Geruchserkennung task.
    """
    aufgabenstellung = StringField('')
    proben = FieldList(StringField(''))
    ohne_auswahl = FieldList(StringField('Geruchserkennung ohne Auswahl', validators=[DataRequired()]))
    mit_auswahl = FieldList(SelectField('Geruchserkennung mit Auswahl', choices=[]))


class ViewDreieckstest(FlaskForm):
    """
    Form for viewing Dreieckstest task.
    """
    aufgabenstellung = StringField('')
    proben_1 = FieldList(StringField(''))
    proben_2 = FieldList(StringField(''))
    abweichende_probe_1 = SelectField('Welches ist die abweichende Probe ?', choices=[])
    abweichende_probe_2 = SelectField('Welches ist die abweichende Probe ?', choices=[])
    beschreibung_1 = StringField('Beschreibung des Unterschieds: ')
    beschreibung_2 = StringField('Beschreibung des Unterschieds: ')


class ViewAuswahltest(FlaskForm):
    """
    Form for viewing Auswahltest task.
    """
    aufgabenstellung = StringField('')
    proben = FieldList(StringField(''))
    einordnungen = FieldList(SelectField('Einordnung', choices=[]))
    bemerkungen = FieldList(StringField('Bemerkung'))


class ViewRangordnungstest(FlaskForm):
    """
    Form for viewing Rangordnungstest task.
    """
    aufgabenstellung = StringField('')
    proben = FieldList(StringField(''))
    ränge = FieldList(SelectField('', choices=[]))


class ViewEbp(FlaskForm):
    """
    Form for viewing Ebp task.
    """
    aufgabenstellung = StringField('')
    proben_nr = StringField('')
    aussehen_farbe = StringField('Farbe: ', validators=[DataRequired()])
    geruch = StringField('Geruch: ', validators=[DataRequired()])
    geschmack = StringField('Geschmack: ', validators=[DataRequired()])
    textur = StringField('Textur: ', validators=[DataRequired()])
    konsistenz = StringField('Konsistenz: ', validators=[DataRequired()])


class TrainingsViewForm(FlaskForm):
    """
    Form for viewing Trainings.
    """
    trainings = SelectField('Trainings', choices=[])
    delete = SubmitField('Löschen')

    def __init__(self, *args, **kwargs):
        super(TrainingsViewForm, self).__init__(*args, **kwargs)
        self.trainings.choices = [(t.id, t.name) for t in Trainings.query.all()]
