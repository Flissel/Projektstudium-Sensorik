from flask import Flask, render_template,render_template_string, request, session, redirect, url_for ,flash, jsonify,copy_current_request_context
from flask_sqlalchemy import SQLAlchemy
from model import db, Trainings, Ebp, Rangordnungstest, Benutzer, Proben, Dreieckstest, Auswahltest, Paar_vergleich, Konz_reihe, Hed_beurteilung, Profilprüfung, Geruchserkennung, Aufgabenstellungen
from forms import CreateTrainingForm, CreateEbpForm, CreateRangordnungstestForm, ModifyForm, TrainingsViewForm, ViewPaar_vergleich
from uuid import uuid4
from threading import Thread
import time


app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/praktikum_db'
app.config['SECRET_KEY'] = 'secret_key'
db.init_app(app)



@app.template_global()
def render_ebp(ebp_question):
    return render_template_string(
        """
        <div class="question-form">
        {{ question.proben_id.label }}
        {{ question.proben_id }}
        </div>
        """
, question=ebp_question)

@app.template_global()
def render_rangordnungstest(rangordnungstest_question):
    return render_template_string(
        """
        <div class="question-form">
            {{ question.proben_id_1.label }}
            {{ question.proben_id_1 }}
            {{ question.proben_id_2.label }}
            {{ question.proben_id_2 }}
            {{ question.proben_id_3.label }}
            {{ question.proben_id_3 }}
            {{ question.proben_id_4.label }}
            {{ question.proben_id_4 }}
            {{ question.proben_id_5.label }}
            {{ question.proben_id_5 }}
        </div>
        """
, question=rangordnungstest_question)

@app.route('/add_question', methods=['POST', 'GET'])
def add_question():
    if request.method == 'POST':
        question_type = request.form.get('question_type')
        if question_type == "ebp":
            request.form.ebp_questions.append_entry()
        else:
            if question_type == "rangordnungstest":
                request.form.rangordnungstest_questions.append_entry()
        
        return render_template("create_training.html", form=request.form)
            
        
        


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This function handles the login process.

    If the user submits a valid username and password, they are redirected to the professor dashboard.
    If the user submits an invalid username or password, they are returned to the login page with an error message.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Benutzer.query.filter_by(benutzername=username).first()

        if user and user.passwort == password:
            session['username'] = user.benutzername
            session['role'] = user.rolle
            if user.rolle == True:
                return redirect(url_for('professor_dashboard'))
            else:
                return redirect(url_for('student_waitingroom'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This function handles the registration process.

    If the user submits a valid username and password, a new user is created in the database and they are redirected to the login page.
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        
        new_user = Benutzer(benutzername=username, passwort=password, rolle=False)
        db.session.add(new_user)
        db.session.commit()
        
        flash(f"User '{username}' has been added to the database!", 'success')
        return redirect(url_for('login'))
    
    return render_template('registery.html')

@app.route('/student_waitingroom')
def student_waitingroom():
    """
    This function handles the student waiting room page.

    If the user is logged in as a student, they are shown the page with the training they are assigned to.
    If the user is not logged in as a student, they are redirected to the login page.
    """
    if 'username' not in session:
        return redirect(url_for('login'))
    
    while True:
        user = Benutzer.query.filter_by(benutzername=session['username']).first()
        if user.rolle == False and user.training_id:
            return redirect(url_for('training_page'))
    
    """

    training_available = False  # A flag to signal if training is available

    @copy_current_request_context
    def check_training(role):
        nonlocal training_available
        if role == False:
            while True:
                user = Benutzer.query.filter_by(benutzername=session['username']).first()
                if user and user.training_id:
                    training_available = True
                    break
                time.sleep(1)
    
    role = session['role']
    Thread(target=check_training, args=(role,)).start()

    if training_available:
        return redirect(url_for('training_page'))

    return render_template('student_waitingroom.html')
    """
@app.route('/Error')
def error():
    """
    This function handles the error page.
    """
    return render_template('Error.html')

@app.route('/professor_dashboard', methods=['GET', 'POST'])
def professor_dashboard():
    """
    This function handles the professor dashboard page.
    If the user is logged in as a professor, they are shown the page with the available trainings.
    If the user is logged in as a student, they are redirected to the student waiting room.
    If the user is not logged in, they are redirected to the login page.
    """
    form = TrainingsViewForm()
    if request.method == 'POST' and session.get('form_id') == request.form.get('form_id') and form.trainings.choices: #prevent double submitting and empty submit
        session.pop('form_id', None)
        action = request.form.get('action')
        if action.startswith("select"):
            students = Benutzer.query.filter_by(rolle=False).all()
            for student in students:
                student.training_id = form.trainings.choices[int(action.split(" ")[1])][0]
                db.session.commit()
        if action.startswith("delete"):
            training = Trainings.query.filter_by(id=form.trainings.choices[int(action.split(" ")[1])][0]).first()
            db.session.delete(training)
            db.session.commit()
        redirect(url_for('professor_dashboard'))

    if 'username' in session:
        username = session['username']
        user = Benutzer.query.filter_by(benutzername=username).first()
        if user.rolle == True:
            form.trainings = Trainings.query.all()
            form_id = str(uuid4()) #Create "form_id"
            session['form_id'] = form_id #Add "form_id" to session
            return render_template('professor_dashboard.html', form=form, form_id=form_id)
        elif user.rolle == False:
            return redirect(url_for('student_waitingroom'))
    return redirect(url_for('login'))

@app.context_processor
def utility_processor():
    def get_attribute(obj, attr):
        return getattr(obj, attr)
    return dict(get_attribute=get_attribute)


@app.route('/professor_dashboard/create_training', methods=['GET', 'POST'])
def create_training():
    """
    This function adds the ability for the professor to create trainings.
    A training can consist of multiple question_types.
    When a training is created all the data is saved to the database.
    """

    #TODO: Die anderen fragentypen hinzufügen

    form = CreateTrainingForm()

    #if form.validate_on_submit():
    if request.method == "POST" and form.data["submit"] == True:
        if form.ebp_questions or form.rangordnungstest_questions or form.auswahltest_questions or form.dreieckstest_questions or form.geruchserkennung_questions or form.hed_beurteilung_questions or form.konz_reihe_questions or form.paar_vergleich_questions or form.profilprüfung_questions:
            print("Form validated successfully")
            fragen_ids = []
            fragen_typen = []

            for question_form in form.ebp_questions:
                proben_id = question_form.proben_id.data
                aufgabenstellung_id = question_form.aufgabenstellung_id.data
                test = Ebp(proben_id=proben_id, aufgabenstellung_id=aufgabenstellung_id)
                
                db.session.add(test)
                db.session.commit()

                fragen_ids.append(test.id)
                fragen_typen.append("ebp")

            for question_form in form.rangordnungstest_questions:
                probenreihe_id = question_form.probenreihe_id.data
                aufgabenstellung_id = question_form.aufgabenstellung_id.data

                test = Rangordnungstest(aufgabenstellung_id=aufgabenstellung_id, probenreihe_id=probenreihe_id)
                db.session.add(test)
                db.session.commit()

                fragen_ids.append(test.id)
                fragen_typen.append("rangordnungstest")
                
            for question_form in form.auswahltest_questions:
                probenreihe_id = question_form.probenreihe_id.data
                aufgabenstellung_id = question_form.aufgabenstellung_id.data

                test = Auswahltest(aufgabenstellung_id=aufgabenstellung_id, probenreihe_id=probenreihe_id)
                db.session.add(test)
                db.session.commit()

                fragen_ids.append(test.id)
                fragen_typen.append("auswahltest")

            for question_form in form.dreieckstest_questions:
                probenreihe_id_1 = question_form.probenreihe_id_1.data
                probenreihe_id_2 = question_form.probenreihe_id_2.data
                aufgabenstellung_id = question_form.aufgabenstellung_id.data
                lösung_1 = question_form.lösung_1.data
                lösung_2 = question_form.lösung_2.data

                test = Dreieckstest(aufgabenstellung_id=aufgabenstellung_id, probenreihe_id_1=probenreihe_id_1, probenreihe_id_2=probenreihe_id_2, lösung_1=lösung_1, lösung_2=lösung_2)
                db.session.add(test)
                db.session.commit()

                fragen_ids.append(test.id)
                fragen_typen.append("dreieckstest") 
                
            for question_form in form.geruchserkennung_questions:
                proben_id = question_form.proben_id.data
                aufgabenstellung_id = question_form.aufgabenstellung_id.data

                test = Geruchserkennung(aufgabenstellung_id=aufgabenstellung_id, proben_id=proben_id)
                db.session.add(test)
                db.session.commit()

                fragen_ids.append(test.id)
                fragen_typen.append("geruchserkennungtest")
            
            for question_form in form.hed_beurteilung_questions:
                probenreihe_id = question_form.probenreihe_id.data
                aufgabenstellung_id = question_form.aufgabenstellung_id.data

                test = Hed_beurteilung(aufgabenstellung_id=aufgabenstellung_id, probenreihe_id=probenreihe_id)
                db.session.add(test)
                db.session.commit()

                fragen_ids.append(test.id)
                fragen_typen.append("hed_beurteilung")
                
            for question_form in form.konz_reihe_questions:
                probenreihe_id = question_form.probenreihe_id.data
                aufgabenstellung_id = question_form.aufgabenstellung_id.data

                test = Konz_reihe(aufgabenstellung_id=aufgabenstellung_id, probenreihe_id=probenreihe_id)
                db.session.add(test)
                db.session.commit()

                fragen_ids.append(test.id)
                fragen_typen.append("konz_reihe")
                
            for question_form in form.paar_vergleich_questions:
                probenreihe_id_1 = question_form.probenreihe_id_1.data
                probenreihe_id_2 = question_form.probenreihe_id_2.data
                aufgabenstellung_id = question_form.aufgabenstellung_id.data
                lösung_1 = question_form.lösung_1.data
                lösung_2 = question_form.lösung_2.data

                test = Paar_vergleich(aufgabenstellung_id=aufgabenstellung_id, probenreihe_id_1=probenreihe_id_1, probenreihe_id_2=probenreihe_id_2, lösung_1=lösung_1, lösung_2=lösung_2)
                db.session.add(test)
                db.session.commit()

                fragen_ids.append(test.id)
                fragen_typen.append("paar_vergleich")
            
            for question_form in form.profilprüfung_questions:
                proben_id = question_form.proben_id.data
                aufgabenstellung_id = question_form.aufgabenstellung_id.data
                kriterien = question_form.kriterien.data

                test = Profilprüfung(aufgabenstellung_id=aufgabenstellung_id, proben_id=proben_id, kriterien=kriterien)
                db.session.add(test)
                db.session.commit()

                fragen_ids.append(test.id)
                fragen_typen.append("profilprüfung")
            
            training = Trainings(
                name=form.name.data,
                fragen_ids = fragen_ids,
                fragen_typen = fragen_typen
            )
            db.session.add(training)
            db.session.commit()

            return redirect(url_for('professor_dashboard'))

    if request.method == "POST" and form.question_types[0].data["add"] == True:
        if form.question_types[0].data["question_type"] == "ebp":
            form.ebp_questions.append_entry()
        if form.question_types[0].data["question_type"] == "rangordnungstest":
            form.rangordnungstest_questions.append_entry()
        if form.question_types[0].data["question_type"] == "auswahltest":
            form.auswahltest_questions.append_entry()
        if form.question_types[0].data["question_type"] == "dreieckstest":
            form.dreieckstest_questions.append_entry()
        if form.question_types[0].data["question_type"] == "geruchserkennung":
            form.geruchserkennung_questions.append_entry()
        if form.question_types[0].data["question_type"] == "hed_beurteilung":
            form.hed_beurteilung_questions.append_entry()
        if form.question_types[0].data["question_type"] == "konz_reihe":
            form.konz_reihe_questions.append_entry()
        if form.question_types[0].data["question_type"] == "paar_vergleich":
            form.paar_vergleich_questions.append_entry()
        if form.question_types[0].data["question_type"] == "profilprüfung":
            form.profilprüfung_questions.append_entry()
    if request.method == "POST" and request.form.get('action'):
        action = request.form.get('action').split(" ", 2)
        print(action[2])
        if action[1] == "ebp":
            ebp1 = form.ebp_questions[0:int(action[2])]
            ebp2 = form.ebp_questions[int(action[2])+1:len(form.ebp_questions)]
            form.ebp_questions = []
            for item in ebp1:
                form.ebp_questions.append(item)
            for item in ebp2:
                form.ebp_questions.append(item)
        if action[1] == "rang":
            rang1 = form.rangordnungstest_questions[0:int(action[2])]
            rang2 = form.rangordnungstest_questions[int(action[2])+1:len(form.rangordnungstest_questions)]
            form.rangordnungstest_questions = []
            for item in rang1:
                form.rangordnungstest_questions.append(item)
            for item in rang2:
                form.rangordnungstest_questions.append(item)
        if action[1] == "auswahltest":
            rang1 = form.auswahltest_questions[0:int(action[2])]
            rang2 = form.auswahltest_questions[int(action[2])+1:len(form.auswahltest_questions)]
            form.auswahltest_questions = []
            for item in rang1:
                form.auswahltest_questions.append(item)
            for item in rang2:
                form.auswahltest_questions.append(item)
        if action[1] == "dreieckstest":
            rang1 = form.dreieckstest_questions[0:int(action[2])]
            rang2 = form.dreieckstest_questions[int(action[2])+1:len(form.dreieckstest_questions)]
            form.dreieckstest_questions = []
            for item in rang1:
                form.dreieckstest_questions.append(item)
            for item in rang2:
                form.dreieckstest_questions.append(item)
        if action[1] == "geruchserkennung":
            rang1 = form.geruchserkennung_questions[0:int(action[2])]
            rang2 = form.geruchserkennung_questions[int(action[2])+1:len(form.geruchserkennung_questions)]
            form.geruchserkennung_questions = []
            for item in rang1:
                form.geruchserkennung_questions.append(item)
            for item in rang2:
                form.geruchserkennung_questions.append(item)
        if action[1] == "hed_beurteilung":
            rang1 = form.hed_beurteilung_questions[0:int(action[2])]
            rang2 = form.hed_beurteilung_questions[int(action[2])+1:len(form.hed_beurteilung_questions)]
            form.hed_beurteilung_questions = []
            for item in rang1:
                form.hed_beurteilung_questions.append(item)
            for item in rang2:
                form.hed_beurteilung_questions.append(item)
        if action[1] == "konz_reihe":
            rang1 = form.konz_reihe_questions[0:int(action[2])]
            rang2 = form.konz_reihe_questions[int(action[2])+1:len(form.konz_reihe_questions)]
            form.konz_reihe_questions = []
            for item in rang1:
                form.konz_reihe_questions.append(item)
            for item in rang2:
                form.konz_reihe_questions.append(item)
        if action[1] == "paar_vergleich":
            rang1 = form.paar_vergleich_questions[0:int(action[2])]
            rang2 = form.paar_vergleich_questions[int(action[2])+1:len(form.paar_vergelich_questions)]
            form.paar_vergleich_questions = []
            for item in rang1:
                form.paar_vergleich_questions.append(item)
            for item in rang2:
                form.paar_vergelich_questions.append(item)
        if action[1] == "profilprüfung":
            rang1 = form.profilprüfung_questions[0:int(action[2])]
            rang2 = form.profilprüfung_questions[int(action[2])+1:len(form.profilprüfung_questions)]
            form.profilprüfung_questions = []
            for item in rang1:
                form.profilprüfung_questions.append(item)
            for item in rang2:
                form.profilprüfung_questions.append(item)

        form.question_types[0].data["submit"] = False
    if request.method == "POST" and request.form.get('kriteria'):
        action = request.form.get('kriteria').split(' ',2)
        if action[0] == 'add':
            form.profilprüfung_questions[int(action[1])].kriterien.append_entry()
        if action[0] == 'remove':
            form.profilprüfung_questions[int(action[1])].kriterien = form.profilprüfung_questions[int(action[1])].kriterien[0:len(form.profilprüfung_questions[int(action[1])].kriterien) -1]
    print("Form validated unsuccessful")
    return render_template('create_training.html', form=form)






@app.route('/select_training/<training>')
def select_training(training):
    """
    This function handles the selection of a training by a professor.
    It sets the 'training' attribute of all students to the selected training.
    After updating the database, it redirects to the training page for the selected training.
    """
    students = Benutzer.query.filter_by(rolle=False).all()
    for student in students:
        student.training = training
        db.session.commit()
    return redirect(url_for('training_progress', question=get_questions(training), students=students))                                  



@app.route('/training_page/', methods=['GET', 'POST'])
def training_page():
    '''
    This function handles the training page for a selected training.
    If the user is not logged in, they are redirected to the login page.
    '''
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        pass

    training = Trainings.query.filter_by(id=Benutzer.query.filter_by(benutzername=session['username']).first().training_id).first()
    question_index = session.get('question_index', 0)
    if not question_index:
        session['question_index'] = 0
    question_type = training.fragen_typen[question_index]
    if question_type:
        if question_type == "paar_vergleich":
            form = ViewPaar_vergleich()
            question = Paar_vergleich.query.filter_by(id=training.fragen_ids[question_index]).first()
            aufgabenstellung = Aufgabenstellungen.query.get(question.aufgabenstellung_id)
            return render_template('training_page.html', question=question, question_type=question_type, form=form, aufgabenstellung=aufgabenstellung)
    return redirect(url_for('login'))




@app.route('/training_progress/<question>')
def training_progress(question):
    
    return render_template('training_progress.html', question=question)

@app.route('/')
def dashboard():
    """
    This function handles the main dashboard page.
    """
    if 'username' not in session:
        return render_template('login.html')
    if Benutzer.query.filter_by(benutzername=session.get('username')).first().rolle == True:
        return redirect(url_for('professor_dashboard'))
    else:
        return redirect(url_for('student_waitingroom'))

"""
def get_questions(training):
    questionlist = []
    questions = multiplechoice_aufgaben.query.all()
    for q in questions:
        question = {
            'id': q.id,
            'question': q.question,
            'options': [q.option1, q.option2, q.option3, q.option4],
            'answer': q.answer
        }
        print(question)
        questionlist.append(question)
    return questionlist
"""


      


if __name__ == '__main__':
    app.run(debug=True)