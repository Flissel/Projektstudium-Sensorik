from flask_wtf import FlaskForm
from flask import request, session
from wtforms import StringField, IntegerField, SubmitField, SelectField, FieldList, FormField, HiddenField,BooleanField
from wtforms.validators import DataRequired, NumberRange
from model import Trainings, Aufgabenstellungen, Probenreihen, Proben, Benutzer,Paar_vergleich, Probenreihen
from wtforms.validators import ValidationError


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
    probenreihe_id = SelectField('Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateKonz_reihe, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="konz_reihe").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class CreateHed_beurteilung(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateHed_beurteilung, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="hed_beurteilung").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class CreateGeruchserkennung(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id = SelectField('Probenreihe', choices=[])
    geruchsauswahl = SelectField('Geruchsauswahl (Irrelevant bei Test ohne Auswahlliste)', choices=[])

    def __init__(self, *args, **kwargs):
        super(CreateGeruchserkennung, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="geruchserkennung").all()]
        self.probenreihe_id.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.geruchsauswahl.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

class CreateDreieckstest(FlaskForm):
    aufgabenstellung_id = SelectField('Aufgabenstellung', choices=[])
    probenreihe_id_1 = SelectField('Probenreihe 1', choices=[])
    probenreihe_id_2 = SelectField('Probenreihe 2', choices=[])


    def __init__(self, *args, **kwargs):
        super(CreateDreieckstest, self).__init__(*args, **kwargs)
        self.aufgabenstellung_id.choices = [(a.id, a.aufgabenstellung) for a in Aufgabenstellungen.query.filter_by(aufgabentyp="dreieckstest").all()]
        self.probenreihe_id_1.choices = [(p.id, p.name) for p in Probenreihen.query.all()]
        self.probenreihe_id_2.choices = [(p.id, p.name) for p in Probenreihen.query.all()]

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
    trainings = SelectField('Trainings', choices=[])
    delete = SubmitField('Löschen')

    def __init__(self, *args, **kwargs):
        super(TrainingsViewForm, self).__init__(*args, **kwargs)
        self.trainings.choices = [(t.id, t.name) for t in Trainings.query.all()]

###################################
#---View Forms for the students---#
###################################

class ViewProfilprüfung(FlaskForm):
    aufgabenstellung = StringField('')
    probe = StringField('')
    kriterien = FieldList(StringField(''))
    skalenwerte = FieldList(SelectField('', choices=[('0', '0 (zu schwach)'),('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9','9'), ('10', '10 (zu stark)')]))

class ViewPaar_vergleich(FlaskForm):
    aufgabenstellung = StringField('')
    proben_1 = FieldList(StringField(''))
    proben_2 = FieldList(StringField(''))
    ausgeprägte_probe_1 = SelectField('Der Geschmack welcher Probe ist stärker ausgeprägt ?', choices=[])
    ausgeprägte_probe_2 = SelectField('Der Geschmack welcher Probe ist stärker ausgeprägt ?', choices=[])
    bemerkung_1 = StringField('Bemerkung: ')
    bemerkung_2 = StringField('Bemerkung: ')
    erwartung_probe = SelectField('Der Geschmack welcher Probe entspricht eher Ihren Erwartungen an das Produkt ?', choices=[])


class ViewKonz_reihe(FlaskForm):
    aufgabenstellung = StringField('')
    proben = FieldList(StringField(''))
    konzentration = FieldList(SelectField('Konzentration: ', choices=[("0", "0"), ("?", "?"), ("X", "X"), ("XX", "XX"), ("XXX", "XXX")]))
    bemerkungen = FieldList(StringField('Anmerkung: '))

class ViewHed_beurteilung(FlaskForm):
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
    aufgabenstellung = StringField('')
    proben = FieldList(StringField(''))
    ohne_auswahl = FieldList(StringField('Geruchserkennung ohne Auswahl', validators=[DataRequired()]))
    mit_auswahl = FieldList(SelectField('Geruchserkennung mit Auswahl', choices=[]))

class ViewDreieckstest(FlaskForm):
    aufgabenstellung = StringField('')
    proben_1 = FieldList(StringField(''))
    proben_2 = FieldList(StringField(''))
    abweichende_probe_1 = SelectField('Welches ist die abweichende Probe ?', choices=[])
    abweichende_probe_2 = SelectField('Welches ist die abweichende Probe ?', choices=[])
    beschreibung_1 = StringField('Beschreibung des unterschieds: ')
    beschreibung_2 = StringField('Beschreibung des unterschieds: ')

class ViewAuswahltest(FlaskForm):
    aufgabenstellung = StringField('')
    proben = FieldList(StringField(''))
    einordnungen = FieldList(SelectField('Einordnung', choices=[]))
    bemerkungen = FieldList(StringField('Bemerkung'))

class ViewRangordnungstest(FlaskForm):
    aufgabenstellung = StringField('')
    proben = FieldList(StringField(''))
    ränge = FieldList(SelectField('', choices=[]))

class ViewEbp(FlaskForm):
    aufgabenstellung = StringField('')
    proben_nr = StringField('')
    aussehen_farbe = StringField('Farbe: ', validators=[DataRequired()])
    geruch = StringField('Geruch: ', validators=[DataRequired()])
    geschmack = StringField('Geschmack: ', validators=[DataRequired()])
    textur = StringField('Textur: ', validators=[DataRequired()])
    konsistenz = StringField('Konsistenz: ', validators=[DataRequired()])

#######################################################
class SubmitEbpForm(FlaskForm):
    aussehen_farbe = StringField('Farbe')
    geruch = StringField('Geruch')
    geschmack = StringField('Geschmack')
    textur = StringField('Textur')
    konsistenz = StringField('Konsistenz')
    csrf_token = HiddenField()

class SubmitProfilprüfung(FlaskForm):
    csrf_token = HiddenField()
    skalenwerte = FieldList(IntegerField('Skalenwert'))
  
class SubmitPaar_vergleich(FlaskForm):
    csrf_token = HiddenField()
    probe_1 = SelectField('Probe 1', choices=[], validators=[DataRequired()], coerce=int)
    probe_2 = SelectField('Probe 2', choices=[], validators=[DataRequired()], coerce=int)
    probe_3 = SelectField('Probe 3', choices=[], validators=[DataRequired()], coerce=int)
    probe_4 = SelectField('Probe 4', choices=[], validators=[DataRequired()], coerce=int)
    probe_5 = SelectField('Probe 5', choices=[], validators=[DataRequired()], coerce=int)
    probe_6 = SelectField('Probe 6', choices=[], validators=[DataRequired()], coerce=int)
    
    def __init__(self, probenreihen_id_1, probenreihen_id_2, *args, **kwargs):
        super(SubmitPaar_vergleich, self).__init__(*args, **kwargs)
        
        self.probe_1.choices = [(probe.proben_nr, probe.proben_nr) for probe in probenreihen_id_1]
        self.probe_2.choices = [(probe.proben_nr, probe.proben_nr) for probe in probenreihen_id_1]
        self.probe_3.choices = [(probe.proben_nr, probe.proben_nr) for probe in probenreihen_id_1]
        self.probe_4.choices = [(probe.proben_nr, probe.proben_nr) for probe in probenreihen_id_2]
        self.probe_5.choices = [(probe.proben_nr, probe.proben_nr) for probe in probenreihen_id_2]
        self.probe_6.choices = [(probe.proben_nr, probe.proben_nr) for probe in probenreihen_id_2]

class SubmitKonz_reihe(FlaskForm):
    gemschmack = StringField('erkannte_geschmacksart')
    stammlösung = StringField('stammlösung')
    antworten = FieldList(SelectField('probenreihen_id'))

class ProbeForm(FlaskForm):
    taste = IntegerField('Taste Evaluation', validators=[DataRequired()])
    
class SubmitHed_beurteilung(FlaskForm):
   
    skalenwerte = FieldList(IntegerField('Skalenwert'))
    csrf_token = HiddenField(validators=[DataRequired()])

class SubmitGeruchserkennung(FlaskForm):
    ohne_auswahl = StringField('Geruchserkennung ohne Auswahl')
    beschreibung = StringField('Beschreibung des Geruchs')
    mit_auswahl = StringField('Geruchserkennung mit Auswahl')
    csrf_token = HiddenField()
        # Add choices for the dynamic fields based on the user's selections

class SubmitDreieckstest(FlaskForm):
    beschreibung_1 = StringField('Beschreibung des Unterschieds (1)')
    beschreibung_2 = StringField('Beschreibung des Unterschieds (2)')
    antwort_1 = StringField('Ihre Antwort (Probe 1)')
    antwort_2 = StringField('Ihre Antwort (Probe 2)')
    csrf_token = HiddenField()
        # Add choices for the dynamic fields based on the user's selections

class SubmitAuswahltest(FlaskForm):
    probe_name = FieldList(StringField())
    probe_nr = FieldList(StringField())
    taste_salzig = FieldList(BooleanField("salzig"))
    taste_süß = FieldList(BooleanField("süß"))
    taste_sauer = FieldList(BooleanField("sauer"))
    taste_bitter = FieldList(BooleanField("bitter"))
    taste_nicht_erkennen = FieldList(BooleanField("nicht zu erkennen"))
    csrf_token = HiddenField()

    def __init__(self, proben=None, proben_nr=None, *args, **kwargs):
        super(SubmitAuswahltest, self).__init__(*args, **kwargs)
        if proben:
            self.probe_name.process(None, data=proben)
        if proben_nr:
            self.probe_nr.process(None, data=proben_nr)

        self.taste_salzig.process(None, data=[0,0,0])    
        self.taste_süß.process(None, data=[0,0,0])
        self.taste_sauer.process(None, data=[0,0,0])
        self.taste_bitter.process(None, data=[0,0,0])
        self.taste_nicht_erkennen.process(None, data=[0,0,0])
        
class SubmitRangordnungstest(FlaskForm):
    antworten = FieldList(HiddenField('Antworten'))   
    csrf_token = HiddenField()
