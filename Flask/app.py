
from flask import Flask, jsonify, render_template, request, session, redirect, url_for ,flash, request

from model import db, Trainings, Ebp, Rangordnungstest, Benutzer, Proben, Probenreihen, Dreieckstest, Auswahltest, Paar_vergleich, Konz_reihe, Hed_beurteilung, Profilprüfung, Geruchserkennung, Aufgabenstellungen
from forms import CreateTrainingForm, CreateEbpForm, CreateRangordnungstestForm, TrainingsViewForm, ViewPaar_vergleich, ViewAuswahltest, ViewDreieckstest, ViewEbp, ViewGeruchserkennung, ViewHed_beurteilung, ViewKonz_reihe, ViewProfilprüfung, ViewRangordnungstest

from uuid import uuid4

import time

from wtforms import SubmitField

app = Flask(__name__)
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/praktikum_db'
app.config['SECRET_KEY'] = 'secret_key'
db.init_app(app)

def zip_lists(a, b):
    return zip(a, b)

app.jinja_env.filters['zip_lists'] = zip_lists

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
                user.aktiv = True
                db.session.commit()
                
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
        
        
        new_user = Benutzer(benutzername=username, passwort=password, rolle=False, aktiv=False)
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
  
    user = Benutzer.query.filter_by(benutzername=session['username']).first()

    if user.rolle == False and user.training_id != None and user.aktiv == True:
      
        return redirect(url_for('training_page')) 
    while True:
        user = Benutzer.query.filter_by(benutzername=session['username']).first()
        if user.rolle == True:
            return redirect(url_for('professor_dashboard'))
        else:
            if user.training_id and user.aktiv == True:
                return redirect(url_for('training_page'))
        time.sleep(1)
        return render_template('student_waitingroom.html')

@app.route('/Error')
def error():
    """
    This function handles the error page.
    """
    return render_template('Error.html')

@app.route('/modify_training/<int:training_id>', methods=['GET', 'POST'])
def modify_training(training_id=None, value=None):
    form = CreateTrainingForm()
    question_types_map = {
        "ebp": form.ebp_questions,
        "rangordnungstest": form.rangordnungstest_questions,
        "auswahltest": form.auswahltest_questions,
        "dreieckstest": form.dreieckstest_questions,
        "geruchserkennung": form.geruchserkennung_questions,
        "hed_beurteilung": form.hed_beurteilung_questions,
        "konz_reihe": form.konz_reihe_questions,
        "paar_vergleich": form.paar_vergleich_questions,
        "profilprüfung": form.profilprüfung_questions
    }
    training = Trainings.query.filter_by(id=training_id).first()
    training_questions = training.fragen_ids
    training_question_types = training.fragen_typen
    form.name.data = training.name
    
    if form.validate_on_submit():
        
        if 'add_question' in request.form:
            question_type = form.question_types.data
            if question_type in question_types_map:
                question_types_map[question_type].append_entry()
                return render_template('modify_training.html', form=form, training_id=training_id)

        for question_type in question_types_map.keys():
            if 'delete_{}_question'.format(question_type) in request.form:
                index_to_remove = int(request.form['delete_{}_question'.format(question_type)])
                question_types_map[question_type].entries.pop(index_to_remove)
                return render_template('modify_training.html', form=form, training_id=training_id)
        
        if 'criteria' in request.form:
            actions = request.form['criteria'].split(' ',2)
            operation = actions[0]
            index = int(actions[1])
            
            if operation == 'add':
                form.profilprüfung_questions[index].kriterien.append_entry()    
            elif operation == 'remove':
                form.profilprüfung_questions[index].kriterien.entries.pop()
            return render_template('modify_training.html', form=form, training_id=training_id)
                
        if 'submit' in request.form:
            
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
                name=request.form["name"],
                fragen_ids = fragen_ids,
                fragen_typen = fragen_typen
            )
            db.session.add(training)
            db.session.commit()

            #TODO: delete training with training_id and all the questions dependend on it
            training_to_delete = Trainings.query.filter_by(id=training_id).first()
            for i in range(len(training_to_delete.fragen_ids)):
                if training_to_delete.fragen_typen[i] == "ebp":
                    Ebp.query.filter_by(id=training_to_delete.fragen_ids[i]).delete()
                if training_to_delete.fragen_typen[i] == "rangordnungstest":
                    Rangordnungstest.query.filter_by(id=training_to_delete.fragen_ids[i]).delete()
                if training_to_delete.fragen_typen[i] == "dreieckstest":
                    Dreieckstest.query.filter_by(id=training_to_delete.fragen_ids[i]).delete()
                if training_to_delete.fragen_typen[i] == "geruchserkennungtest":
                    Geruchserkennung.query.filter_by(id=training_to_delete.fragen_ids[i]).delete()
                if training_to_delete.fragen_typen[i] == "hed_beurteilung":
                    Hed_beurteilung.query.filter_by(id=training_to_delete.fragen_ids[i]).delete()
                if training_to_delete.fragen_typen[i] == "konz_reihe":
                    Konz_reihe.query.filter_by(id=training_to_delete.fragen_ids[i]).delete()
                if training_to_delete.fragen_typen[i] == "paar_vergleich":
                    Paar_vergleich.query.filter_by(id=training_to_delete.fragen_ids[i]).delete()
                if training_to_delete.fragen_typen[i] == "profilprüfung":
                    Profilprüfung.query.filter_by(id=training_to_delete.fragen_ids[i]).delete()
                
            db.session.delete(training_to_delete)
            db.session.commit()

            flash("Training erfolgreich erstellt", "success")
            return redirect(url_for('professor_dashboard'))
    index = 0       
    for question in training_question_types:
        if question == "ebp":
            form.ebp_questions.append_entry()
            form.ebp_questions[-1].proben_id.data = Ebp.query.filter_by(id=training_questions[index]).first().proben_id
            form.ebp_questions[-1].proben_id.default = Ebp.query.filter_by(id=training_questions[index]).first().proben_id
            form.ebp_questions[-1].aufgabenstellung_id.data = Ebp.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.ebp_questions[-1].aufgabenstellung_id.default = Ebp.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.ebp_questions[-1].form.process()
        if question == "rangordnungstest":
            form.rangordnungstest_questions.append_entry()
            form.rangordnungstest_questions[-1].probenreihe_id.data = Rangordnungstest.query.filter_by(id=training_questions[index]).first().probenreihe_id
            form.rangordnungstest_questions[-1].probenreihe_id.default = Rangordnungstest.query.filter_by(id=training_questions[index]).first().probenreihe_id
            form.rangordnungstest_questions[-1].aufgabenstellung_id.data = Rangordnungstest.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.rangordnungstest_questions[-1].aufgabenstellung_id.default = Rangordnungstest.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.rangordnungstest_questions[-1].form.process()
        if question == "auswahltest":
            form.auswahltest_questions.append_entry()
            form.auswahltest_questions[-1].probenreihe_id.data = Auswahltest.query.filter_by(id=training_questions[index]).first().probenreihe_id
            form.auswahltest_questions[-1].probenreihe_id.default = Auswahltest.query.filter_by(id=training_questions[index]).first().probenreihe_id
            form.auswahltest_questions[-1].aufgabenstellung_id.data = Auswahltest.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.auswahltest_questions[-1].aufgabenstellung_id.default = Auswahltest.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.auswahltest_questions[-1].form.process()
        if question == "dreieckstest":
            form.dreieckstest_questions.append_entry()
            form.dreieckstest_questions[-1].probenreihe_id_1.data = Dreieckstest.query.filter_by(id=training_questions[index]).first().probenreihe_id_1
            form.dreieckstest_questions[-1].probenreihe_id_1.default = Dreieckstest.query.filter_by(id=training_questions[index]).first().probenreihe_id_1
            form.dreieckstest_questions[-1].probenreihe_id_2.data = Dreieckstest.query.filter_by(id=training_questions[index]).first().probenreihe_id_2
            form.dreieckstest_questions[-1].probenreihe_id_2.default = Dreieckstest.query.filter_by(id=training_questions[index]).first().probenreihe_id_2
            form.dreieckstest_questions[-1].aufgabenstellung_id.data = Dreieckstest.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.dreieckstest_questions[-1].aufgabenstellung_id.default = Dreieckstest.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.dreieckstest_questions[-1].lösung_1.data = Dreieckstest.query.filter_by(id=training_questions[index]).first().lösung_1
            form.dreieckstest_questions[-1].lösung_1.default = Dreieckstest.query.filter_by(id=training_questions[index]).first().lösung_1
            form.dreieckstest_questions[-1].lösung_2.data = Dreieckstest.query.filter_by(id=training_questions[index]).first().lösung_2
            form.dreieckstest_questions[-1].lösung_2.default = Dreieckstest.query.filter_by(id=training_questions[index]).first().lösung_2
            form.dreieckstest_questions[-1].form.process()
        if question == "geruchserkennung":
            form.geruchserkennung_questions.append_entry()
            form.geruchserkennung_questions[-1].proben_id.data = Geruchserkennung.query.filter_by(id=training_questions[index]).first().proben_id
            form.geruchserkennung_questions[-1].proben_id.default = Geruchserkennung.query.filter_by(id=training_questions[index]).first().proben_id
            form.geruchserkennung_questions[-1].aufgabenstellung_id.data = Geruchserkennung.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.geruchserkennung_questions[-1].aufgabenstellung_id.default = Geruchserkennung.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.geruchserkennung_questions[-1].form.process()
        if question == "hed_beurteilung":
            form.hed_beurteilung_questions.append_entry()
            form.hed_beurteilung_questions[-1].probenreihe_id.data = Hed_beurteilung.query.filter_by(id=training_questions[index]).first().probenreihe_id
            form.hed_beurteilung_questions[-1].probenreihe_id.default = Hed_beurteilung.query.filter_by(id=training_questions[index]).first().probenreihe_id
            form.hed_beurteilung_questions[-1].aufgabenstellung_id.data = Hed_beurteilung.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.hed_beurteilung_questions[-1].aufgabenstellung_id.default = Hed_beurteilung.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.hed_beurteilung_questions[-1].form.process()
        if question == "konz_reihe":
            form.konz_reihe_questions.append_entry()
            form.konz_reihe_questions[-1].probenreihe_id.data = Konz_reihe.query.filter_by(id=training_questions[index]).first().probenreihe_id
            form.konz_reihe_questions[-1].probenreihe_id.default = Konz_reihe.query.filter_by(id=training_questions[index]).first().probenreihe_id
            form.konz_reihe_questions[-1].aufgabenstellung_id.data = Konz_reihe.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.konz_reihe_questions[-1].aufgabenstellung_id.default = Konz_reihe.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.konz_reihe_questions[-1].form.process()
        if question == "paar_vergleich":
            form.paar_vergleich_questions.append_entry()
            form.paar_vergleich_questions[-1].probenreihe_id_1.data = Paar_vergleich.query.filter_by(id=training_questions[index]).first().probenreihe_id_1
            form.paar_vergleich_questions[-1].probenreihe_id_1.default = Paar_vergleich.query.filter_by(id=training_questions[index]).first().probenreihe_id_1
            form.paar_vergleich_questions[-1].probenreihe_id_2.data = Paar_vergleich.query.filter_by(id=training_questions[index]).first().probenreihe_id_2
            form.paar_vergleich_questions[-1].probenreihe_id_2.default = Paar_vergleich.query.filter_by(id=training_questions[index]).first().probenreihe_id_2
            form.paar_vergleich_questions[-1].aufgabenstellung_id.data = Paar_vergleich.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.paar_vergleich_questions[-1].aufgabenstellung_id.default = Paar_vergleich.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.paar_vergleich_questions[-1].lösung_1.data = Paar_vergleich.query.filter_by(id=training_questions[index]).first().lösung_1
            form.paar_vergleich_questions[-1].lösung_1.default = Paar_vergleich.query.filter_by(id=training_questions[index]).first().lösung_1
            form.paar_vergleich_questions[-1].lösung_2.data = Paar_vergleich.query.filter_by(id=training_questions[index]).first().lösung_2
            form.paar_vergleich_questions[-1].lösung_2.default = Paar_vergleich.query.filter_by(id=training_questions[index]).first().lösung_2
            form.paar_vergleich_questions[-1].form.process()
        if question == "profilprüfung":
            form.profilprüfung_questions.append_entry()
            form.profilprüfung_questions[-1].proben_id.data = Profilprüfung.query.filter_by(id=training_questions[index]).first().proben_id
            form.profilprüfung_questions[-1].proben_id.default = Profilprüfung.query.filter_by(id=training_questions[index]).first().proben_id
            form.profilprüfung_questions[-1].aufgabenstellung_id.data = Profilprüfung.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.profilprüfung_questions[-1].aufgabenstellung_id.default = Profilprüfung.query.filter_by(id=training_questions[index]).first().aufgabenstellung_id
            form.profilprüfung_questions[-1].kriterien.data = Profilprüfung.query.filter_by(id=training_questions[index]).first().kriterien
            form.profilprüfung_questions[-1].kriterien.default = Profilprüfung.query.filter_by(id=training_questions[index]).first().kriterien
            form.profilprüfung_questions[-1].form.process()
        index += 1
    
    return render_template('modify_training.html', form=form, training_id=training_id)

@app.route('/professor_dashboard', methods=['GET', 'POST'])
def professor_dashboard():
    """
    This function handles the professor dashboard page.
    If the user is logged in as a professor, they are shown the page with the available trainings.
    If the user is logged in as a student, they are redirected to the student waiting room.
    If the user is not logged in, they are redirected to the login page.
    """
    form = TrainingsViewForm()
    question_types_map = {
        "ebp": Ebp,
        "rangordnungstest": Rangordnungstest,
        "auswahltest": Auswahltest,
        "dreieckstest": Dreieckstest,
        "geruchserkennung": Geruchserkennung,
        "hed_beurteilung": Hed_beurteilung,
        "konz_reihe": Konz_reihe,
        "paar_vergleich": Paar_vergleich,
        "profilprüfung": Profilprüfung
    }
    
        
    if request.method == 'POST' and session.get('form_id') == request.form.get('form_id') and form.trainings.choices: #prevent double submitting and empty submit
        
        session.pop('form_id', None)
        
        if request.method == 'POST':
            form_id = request.form.get('form_id')
            action = request.form.get('action')

        # Debug print statements
            index = int(action.split(' ')[1])
        if 'select' in request.form['action']:
            students = Benutzer.query.filter_by(rolle=False).all()
            
            print("hi")
            for student in students:
                student.training_id = form.trainings.choices[index][0]
                db.session.commit()

        if 'delete' in request.form['action']:
            
            training = Trainings.query.filter_by(id=form.trainings.choices[index][0]).first()
            for i in range(len(training.fragen_ids)):
                db.session.delete(question_types_map[training.fragen_typen[i]].query.filter_by(id=training.fragen_ids[i]).first())
                db.session.commit()
                
            db.session.delete(training)
            db.session.commit()
            return redirect(url_for('professor_dashboard'))
        
        if 'modify' in request.form['action']:
            
            return redirect(url_for('modify_training', training_id=form.trainings.choices[index][0]))
        
    
    if 'username' in session:
        username = session['username']
        user = Benutzer.query.filter_by(benutzername=username).first()
        if user.rolle == True:
            form.trainings = Trainings.query.all()
            form_id = str(uuid4()) #Create "form_id"
            session['form_id'] = form_id
             #Add "form_id" to session
            return render_template('professor_dashboard.html', form=form, form_id=form_id)
        elif user.rolle == False:
            return redirect(url_for('student_waitingroom'))
    return redirect(url_for('login'))

@app.route('/select_training/<training>')
def select_training(training):
    """
    This function handles the selection of a training by a professor.
    It sets the 'training' attribute of all students to the selected training.
    After updating the database, it redirects to the training page for the selected training.
    """
    students = Benutzer.query.filter_by(rolle=False,aktiv=True).all()
    print(students)
    for student in students:
        student.training = training
        db.session.commit()
    return redirect(url_for('training_progress', students=students))  
                            



@app.route('/professor_dashboard/create_training', methods=['GET', 'POST'])
def create_training():
    """
    This function adds the ability for the professor to create trainings.
    A training can consist of multiple question_types.
    When a training is created all the data is saved to the database.
    """

    #TODO: Die anderen fragentypen hinzufügen

    form = CreateTrainingForm()
    question_types_map = {
    "ebp": form.ebp_questions,
    "rangordnungstest": form.rangordnungstest_questions,
    "auswahltest": form.auswahltest_questions,
    "dreieckstest": form.dreieckstest_questions,
    "geruchserkennung": form.geruchserkennung_questions,
    "hed_beurteilung": form.hed_beurteilung_questions,
    "konz_reihe": form.konz_reihe_questions,
    "paar_vergleich": form.paar_vergleich_questions,
    "profilprüfung": form.profilprüfung_questions,
}

    if form.validate_on_submit():
        
        if 'add_question' in request.form:
            question_type = form.question_types.data
            if question_type in question_types_map:
                question_types_map[question_type].append_entry()

        for question_type in question_types_map.keys():
            if 'delete_{}_question'.format(question_type) in request.form:
                index_to_remove = int(request.form['delete_{}_question'.format(question_type)])
                question_types_map[question_type].entries.pop(index_to_remove)
        
        if 'criteria' in request.form:
            actions = request.form['kriteria'].split(' ',2)
            operation = actions[0]
            index = int(actions[1])
            
            if operation == 'add':
                form.profilprüfung_questions[index].criteria.append_entry()    
            elif operation == 'remove':
                form.profilprüfung_questions[index].criteria.entries.pop()
                
        if 'submit' in request.form:
            
            
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
    """       
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
    """
    if request.method == "POST" and request.form.get('kriteria'):
        action = request.form.get('kriteria').split(' ',2)
        if action[0] == 'add':
            form.profilprüfung_questions[int(action[1])].kriterien.append_entry()
        if action[0] == 'remove':
            form.profilprüfung_questions[int(action[1])].kriterien = form.profilprüfung_questions[int(action[1])].kriterien[0:len(form.profilprüfung_questions[int(action[1])].kriterien) -1]
    print("Form validated unsuccessful")
    return render_template('create_training.html', form=form)


@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    if 'username' not in session:
        return render_template('login.html', error="Bitte loggen Sie sich ein, um auf diese Seite zugreifen zu können.")
    
    task = Aufgabenstellungen.query.get(task_id)
    
    if task is None:
        # Handle case when the task with the specified task_id is not found
        flash("Task not found.", "error")
    else:
        db.session.delete(task)
        db.session.commit()
        flash("Task deleted successfully.", "success")
    
    return redirect(url_for('manage_aufgabenstellungen'))                           
@app.route('/edit_task/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if 'username' not in session:
        return render_template('login.html', error="Bitte loggen Sie sich ein, um auf diese Seite zugreifen zu können.")
    
    task = Aufgabenstellungen.query.get(task_id)
    
    if task is None:
        # Handle case when the task with the specified task_id is not found
        flash("Task not found.", "error")
        return redirect(url_for('manage_aufgabenstellungen'))
    
    if request.method == 'POST':
        aufgabenstellung = request.form.get('aufgabenstellung')
        
        # Perform necessary operations to update the task using 'aufgabenstellung'
        task.aufgabenstellung = aufgabenstellung
        db.session.commit()
        
        # Redirect to the task list page after updating the task
        flash("Task updated successfully.", "success")
        return redirect(url_for('task_list'))
    
    return render_template('edit_task.html', task=task)
@app.route('/create_task/', methods=['GET', 'POST'])
def create_task():
    if 'username' not in session:
        return render_template('login.html', error="Bitte loggen Sie sich ein, um auf diese Seite zugreifen zu können.")
    
    if request.method == 'POST':
        aufgabenstellung = request.form.get('aufgabenstellung')
        
        # Perform necessary operations to create a new task using 'aufgabenstellung'
        # Example code to create a new task using SQLAlchemy
        task = Aufgabenstellungen(aufgabenstellung=aufgabenstellung)
        
        db.session.add(task)
        db.session.commit()
        
        # Redirect to the task list page after creating the task
        flash("Task created successfully.", "success")
        return redirect(url_for('task_list'))
    
    return render_template('create_task.html')

@app.route('/professor_dashboard/manage_aufgabenstellungen/', methods=['GET', 'POST'])
def manage_aufgabenstellungen():
    if 'username' not in session:
        return render_template('login.html', error="Bitte loggen Sie sich ein, um auf diese Seite zugreifen zu können.")
    # Retrieve the data from the database (Example: fetching tasks from the database)
    tasks = Aufgabenstellungen.query.all()
    prüfvariante = request.form.getlist('prüfvariante')
    return render_template('manage_aufgabenstellungen.html', tasks=tasks , prüfvariante=prüfvariante)



@app.route('/training_page/', methods=['GET', 'POST'])
def training_page():
    '''
    This function handles the training page for a selected training.
    If the user is not logged in, they are redirected to the login page.
    '''
    if 'username' not in session:
        return render_template('login.html', error="Bitte loggen Sie sich ein, um auf diese Seite zugreifen zu können.")
   
    if request.method == 'POST':
        pass

    training = Trainings.query.filter_by(id=Benutzer.query.filter_by(benutzername=session['username']).first().training_id).first()
    question_index = session.get('question_index', 0)
    if not question_index:
        session['question_index'] = 0
    question_type = training.fragen_typen[question_index]
    if question_type:
        if question_type == "auswahltest":
            form = ViewAuswahltest()
            question = Auswahltest.query.filter_by(id=training.fragen_ids[question_index]).first()
            aufgabenstellung = Aufgabenstellungen.query.get(question.aufgabenstellung_id)
            probenreihen_id = Probenreihen.query.get(question.probenreihe_id)
            return render_template('training_page.html', question=question, question_type=question_type, form=form, aufgabenstellung=aufgabenstellung, probenreihen_id=probenreihen_id, Proben=Proben)
        if question_type == "dreieckstest":
            form = ViewDreieckstest()
            question = Dreieckstest.query.filter_by(id=training.fragen_ids[question_index]).first()
            aufgabenstellung = Aufgabenstellungen.query.get(question.aufgabenstellung_id)
            probenreihen_id_1 = Probenreihen.query.get(question.probenreihe_id_1)
            probenreihen_id_2 = Probenreihen.query.get(question.probenreihe_id_2)
            return render_template('training_page.html', question=question, question_type=question_type, form=form, aufgabenstellung=aufgabenstellung, probenreihen_id_1=probenreihen_id_1, probenreihen_id_2=probenreihen_id_2, Proben=Proben)
        if question_type == "geruchserkennung":
            form = ViewGeruchserkennung()
            question = Geruchserkennung.query.filter_by(id=training.fragen_ids[question_index]).first()
            aufgabenstellung = Aufgabenstellungen.query.get(question.aufgabenstellung_id)
            proben_id = Proben.query.get(question.proben_id)
            return render_template('training_page.html', question=question, question_type=question_type, form=form, aufgabenstellung=aufgabenstellung, proben_id=proben_id)
        if question_type == "hed_beurteilung":
            form = ViewHed_beurteilung()
            question = Hed_beurteilung.query.filter_by(id=training.fragen_ids[question_index]).first()
            aufgabenstellung = Aufgabenstellungen.query.get(question.aufgabenstellung_id)
            probenreihen_id = Probenreihen.query.get(question.probenreihe_id)
            return render_template('training_page.html', question=question, question_type=question_type, form=form, aufgabenstellung=aufgabenstellung, probenreihen_id=probenreihen_id, Proben=Proben)
        if question_type == "konz_reihe":
            form = ViewKonz_reihe()
            question = Konz_reihe.query.filter_by(id=training.fragen_ids[question_index]).first()
            aufgabenstellung = Aufgabenstellungen.query.get(question.aufgabenstellung_id)
            probenreihen_id = Probenreihen.query.get(question.probenreihe_id)
            return render_template('training_page.html', question=question, question_type=question_type, form=form, aufgabenstellung=aufgabenstellung, probenreihen_id=probenreihen_id, Proben=Proben)
        if question_type == "ebp":
            form = ViewEbp()
            question = Ebp.query.filter_by(id=training.fragen_ids[question_index]).first()
            aufgabenstellung = Aufgabenstellungen.query.get(question.aufgabenstellung_id)
            proben_id = Proben.query.get(question.proben_id)
            return render_template('training_page.html', question=question, question_type=question_type, form=form, aufgabenstellung=aufgabenstellung, proben_id=proben_id, Proben=Proben)
        if question_type == "rangordnungstest":
            form = ViewRangordnungstest()
            question = Rangordnungstest.query.filter_by(id=training.fragen_ids[question_index]).first()
            aufgabenstellung = Aufgabenstellungen.query.get(question.aufgabenstellung_id)
            probenreihen_id = Probenreihen.query.get(question.probenreihe_id)
            for probe in probenreihen_id.proben_ids:
                form.antworten.append_entry()
                
            return render_template('training_page.html', question=question, question_type=question_type, form=form, aufgabenstellung=aufgabenstellung, probenreihen_id=probenreihen_id, Proben=Proben)
        if question_type == "paar_vergleich":
            form = ViewPaar_vergleich()
            question = Paar_vergleich.query.filter_by(id=training.fragen_ids[question_index]).first()
            aufgabenstellung = Aufgabenstellungen.query.get(question.aufgabenstellung_id)
            probenreihen_id_1 = Probenreihen.query.get(question.probenreihe_id_1)
            probenreihen_id_2 = Probenreihen.query.get(question.probenreihe_id_2)
            return render_template('training_page.html', question=question, question_type=question_type, form=form, aufgabenstellung=aufgabenstellung, probenreihen_id_1=probenreihen_id_1, probenreihen_id_2=probenreihen_id_2, Proben=Proben)
        if question_type == "profilprüfung":
            form = ViewProfilprüfung()
            question = Profilprüfung.query.filter_by(id=training.fragen_ids[question_index]).first()
            aufgabenstellung = Aufgabenstellungen.query.get(question.aufgabenstellung_id)
            proben_id = Probenreihen.query.get(question.probenreihe_id_1)
            kriterien = Profilprüfung.query.filter_by(id=training.fragen_ids[question_index]).first().kriterien
            return render_template('training_page.html', question=question, question_type=question_type, form=form, aufgabenstellung=aufgabenstellung, probenreihen_id_1=probenreihen_id_1, probenreihen_id_2=probenreihen_id_2, Proben=Proben)
    return render_template('login.html')

@app.route('/professor_dashboard/training_progress')
def training_progress():
    # get all logged in users
    users = Benutzer.query.all()

    # calculate the progress of each user absolving a training
    user_progress = []
    for user in users:
        progress = calculate_training_progress(user)
        user_progress.append((user, progress))

    # show the training progress of each user
    for user, progress in user_progress:
        print(f"{user.username}: {progress}")

    # give the required data to the template
    return render_template('training_progress.html', user_progress=user_progress)

def calculate_training_progress(user):
    completed_tasks = 0
    total_tasks = 0

    training = Trainings.query.get(user.training_id)

    if training:
        total_tasks = len(training.fragen_ids)

        for fragen_id in training.fragen_ids:
            if check_task_completion(user, fragen_id):
                completed_tasks += 1

    if total_tasks > 0:
        progress = (completed_tasks / total_tasks) * 100
    else:
        progress = 0

    return progress


def check_task_completion(user, fragen_id):
    task_type = Aufgabenstellungen.query.get(fragen_id).aufgabentyp

    if task_type == 'paar_vergleich':
        task = Paar_vergleich.query.filter_by(aufgabenstellung_id=fragen_id).first()
        if task:
            # Assuming user_responses is a relationship between User and Paar_vergleich models
            user_response = task.user_responses.filter_by(user_id=user.id).first()
            if user_response:
                return True

    # Add conditions for other task types as needed

    return False


@app.route('/')
def dashboard():
    """
    This function handles the main dashboard page.
    """
    print(session)
    if 'username' not in session:
        return render_template('login.html')
        
    return render_template('dashboard.html')
@app.route('/view_samples/')
def view_samples():
    # Logic to retrieve sample data
    samples = Proben.query.all()
    sampleChain = Probenreihen.query.all()
    return render_template('view_samples.html', samples=samples , sampleChain=sampleChain)

# Route for editing a sample
@app.route('/edit_sample/<sample_id>', methods=['GET', 'POST'])
def edit_sample(sample_id):
    sample = Proben.query.get(sample_id)

    if request.method == 'POST':
        form_data = request.form
        print(form_data)
        update_sample_in_database(sample_id, form_data)
        return redirect(url_for('view_samples'))

    return render_template('edit_sample.html', sample=sample)

# Helper function to fetch a sample from the database
def fetch_sample_from_database(sample_id):
    sample = Proben.query.get(sample_id)
    
    return sample

# Helper function to update a sample in the database
def update_sample_in_database(sample_id, form_data):
    try:
        sample = Proben.query.get(sample_id)
        if sample is None:
            raise ValueError("Sample not found in the database.")
        

        sample.probenname = form_data.get('probenname')
        sample.proben_nr = form_data.get('proben_nr')
        sample.farbe = form_data.get('farbe')
        sample.farbintensität = form_data.get('farbintensität')
        sample.geruch = form_data.get('geruch')
        sample.geschmack = form_data.get('geschmack')
        sample.textur = form_data.get('textur')
        sample.konsistenz = form_data.get('konsistenz')

        db.session.commit()
    except Exception as e:
        print(f"Error updating sample: {e}")
        db.session.rollback()

@app.route('/create_sample', methods=['GET', 'POST'])
def create_sample():
    if request.method == 'POST':
        form_data = request.form
        # Logic to create a new sample based on form data
        create_sample_in_database(form_data)
        return redirect(url_for('view_samples'))

    return render_template('create_sample.html')
@app.route('/create_sample_chain', methods=['GET', 'POST'])
def create_sample_chain():
    if request.method == 'POST':
        name = request.form['name']
        selected_proben_ids = request.form.getlist('proben_ids[]')  # Use getlist to retrieve all selected IDs

        # Process the selected proben IDs
        proben_ids = []
        for proben_id in selected_proben_ids:
            if proben_id:
                proben = Proben.query.get(proben_id)
                if proben:
                    proben_ids.append(proben_id)

        # Create a new Probenreihen instance
        sample_chain = Probenreihen(name=name, proben_ids=proben_ids)
        
        # Add the new sample chain to the database
        db.session.add(sample_chain)
        db.session.commit()

        flash('Sample chain created successfully!')
        return redirect(url_for('view_samples'))
    
    samples = Proben.query.all()
    return render_template('create_sample_chain.html', samples=samples)

# Delete a sample
@app.route('/delete_sample/<sample_id>', methods=['DELETE'])
def delete_sample(sample_id):
    sample = Proben.query.get(sample_id)
    if sample:
        # TODO: Delete the sample from the database
        db.session.delete(sample)
        db.session.commit()
        return jsonify({'message': 'Sample deleted successfully'})
    else:
        return jsonify({'message': 'Sample not found'})
# Delete a sample chain
@app.route('/delete_sample_chain/<sample_chain_id>', methods=['DELETE'])
def delete_sample_chain(sample_chain_id):
    sample_chain = Probenreihen.query.get(sample_chain_id)
    if sample_chain:
        db.session.delete(sample_chain)
        db.session.commit()
        return jsonify({'message': 'Sample chain deleted successfully'})
    else:
        return jsonify({'message': 'Sample chain not found'})

def create_sample_in_database(form_data):
    """
    Creates a new sample record in the database with the given form data.

    :param form_data: A dictionary containing the form data.
    :type form_data: dict
    :return: None
    """
    proben_nr = form_data.get('proben_nr')
    probenname = form_data.get('probenname')
    farbe = form_data.get('farbe')
    farbintensität = form_data.get('farbintensitaet')
    geruch = form_data.get('geruch')
    geschmack = form_data.get('geschmack')
    textur = form_data.get('textur')
    konsistenz = form_data.get('konsistenz')

    sample = Proben(proben_nr=proben_nr, probenname=probenname, farbe=farbe, farbintensität=farbintensität,
                    geruch=geruch, geschmack=geschmack, textur=textur, konsistenz=konsistenz)

    db.session.add(sample)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True)