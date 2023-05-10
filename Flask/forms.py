from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField, FieldList, FormField, HiddenField
from wtforms.validators import DataRequired

class AddForm(FlaskForm):
    question_type = SelectField("Fragentyp", choices=[('ebp', 'EBP'), ('rangordnungstest', 'Rangordnungstest')], default="ebp")
    submit = SubmitField("Add question")

class RangordnungstestForm(FlaskForm):
    proben_id_1 = SelectField('Proben ID 1')
    proben_id_2 = SelectField('Proben ID 2')
    proben_id_3 = SelectField('Proben ID 3')
    proben_id_4 = SelectField('Proben ID 4')
    proben_id_5 = SelectField('Proben ID 5')

class EbpForm(FlaskForm):
    proben_id = IntegerField('Proben ID')
    aussehen_farbe = StringField('Aussehen/Farbe')
    geruch = StringField('Geruch')
    geschmack = StringField('Geschmack')
    textur = StringField('Textur')
    konsistenz = StringField('Konsistenz')

class CreateTrainingForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    question_types = FieldList(FormField(AddForm), min_entries=1)
    ebp_questions = FieldList(FormField(EbpForm))
    rangordnungstest_questions = FieldList(FormField(RangordnungstestForm))
    submit = SubmitField('Create Training')
