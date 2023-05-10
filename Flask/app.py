from flask import Flask, render_template,render_template_string, request, session, redirect, url_for ,flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from model import db, Trainings, Questions, EBP, Rangordnungstest, Benutzer, Proben
from forms import CreateTrainingForm, EbpForm, RangordnungstestForm, ModifyForm


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
            session['username'] = username
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
    if 'username' in session:
        username = session['username']
        user = Benutzer.query.filter_by(benutzername=username).first()
        if user.rolle == False:
            training = user.training
            return render_template('student_waitingroom.html', training=training)
    return redirect(url_for('login'))

@app.route('/Error')
def error():
    """
    This function handles the error page.
    """
    return render_template('Error.html')

@app.route('/professor_dashboard')
def professor_dashboard():
    """
    This function handles the professor dashboard page.
    If the user is logged in as a professor, they are shown the page with the available trainings.
    If the user is logged in as a student, they are redirected to the student waiting room.
    If the user is not logged in, they are redirected to the login page.
    """
    if 'username' in session:
        username = session['username']
        user = Benutzer.query.filter_by(benutzername=username).first()
        if user.rolle == True:
            trainings = Trainings.query.all()
            return render_template('professor_dashboard.html', trainings=trainings)
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
        print("Form validated successfully")
        question_ids = []

        for ebpForm in form.ebp_questions:
            proben_id = ebpForm.proben_id.data
            ebp = EBP(proben_id=proben_id)
            db.session.add(ebp)
            db.session.commit()

            question = Questions(fragen_typ='ebp', fragen_id=ebp.id)
            db.session.add(question)
            db.session.commit()
            question_ids.append(question.id)

        for rangordnungstestForm in form.rangordnungstest_questions:
            proben_id_1 = rangordnungstestForm.proben_id_1.data
            proben_id_2 = rangordnungstestForm.proben_id_2.data
            proben_id_3 = rangordnungstestForm.proben_id_3.data
            proben_id_4 = rangordnungstestForm.proben_id_4.data
            proben_id_5 = rangordnungstestForm.proben_id_5.data

            rangordnungstest = Rangordnungstest(proben_id_1=proben_id_1, proben_id_2=proben_id_2, proben_id_3=proben_id_3, proben_id_4=proben_id_4, proben_id_5=proben_id_5)
            db.session.add(rangordnungstest)
            db.session.commit()

            question = Questions(fragen_typ='rangordnungstest', fragen_id=rangordnungstest.id)
            db.session.add(question)
            db.session.commit()
            question_ids.append(question.id)
        print(question_ids)
        training = Trainings(
            name=form.name.data,
            question_id_1=question_ids[0] if len(question_ids) > 0 else None,
            question_id_2=question_ids[1] if len(question_ids) > 1 else None,
            question_id_3=question_ids[2] if len(question_ids) > 2 else None,
            question_id_4=question_ids[3] if len(question_ids) > 3 else None,
            question_id_5=question_ids[4] if len(question_ids) > 4 else None,
            question_id_6=question_ids[5] if len(question_ids) > 5 else None,
            question_id_7=question_ids[6] if len(question_ids) > 6 else None,
            question_id_8=question_ids[7] if len(question_ids) > 7 else None,
            question_id_9=question_ids[8] if len(question_ids) > 8 else None,
            question_id_10=question_ids[9] if len(question_ids) > 9 else None,
        )
        db.session.add(training)
        db.session.commit()

        return redirect(url_for('professor_dashboard'))

    if request.method == "POST" and form.question_types[0].data["add"] == True:
        if form.question_types[0].data["question_type"] == "ebp":
            form.ebp_questions.append_entry()
        if form.question_types[0].data["question_type"] == "rangordnungstest":
            form.rangordnungstest_questions.append_entry()
    if request.method == "POST" and form.question_types[0].data["remove"] == True:
        if form.question_types[0].data["question_type"] == "ebp":
            form.ebp_questions = form.ebp_questions[0:len(form.ebp_questions)-1]
        if form.question_types[0].data["question_type"] == "rangordnungstest":
            form.rangordnungstest_questions = form.rangordnungstest_questions[0:len(form.rangordnungstest_questions)-1]
        
        
        
    for ebpForm in form.ebp_questions:
            ebpForm.proben_id.choices = [(record.id, f"{record.proben_nr} - {record.probenname}") for record in Proben.query.all()]
            ebpForm.proben_id.default = ebpForm.proben_id.choices[0]
    for rangordnungstest in form.rangordnungstest_questions:
        rangordnungstest.proben_id_1.choices = [(record.id, f"{record.proben_nr} - {record.probenname}") for record in Proben.query.all()]
        rangordnungstest.proben_id_2.choices = [(record.id, f"{record.proben_nr} - {record.probenname}") for record in Proben.query.all()]
        rangordnungstest.proben_id_3.choices = [(record.id, f"{record.proben_nr} - {record.probenname}") for record in Proben.query.all()]
        rangordnungstest.proben_id_4.choices = [(record.id, f"{record.proben_nr} - {record.probenname}") for record in Proben.query.all()]
        rangordnungstest.proben_id_5.choices = [(record.id, f"{record.proben_nr} - {record.probenname}") for record in Proben.query.all()]
        rangordnungstest.proben_id_1.default = rangordnungstest.proben_id_5.choices[0]
        rangordnungstest.proben_id_2.default = rangordnungstest.proben_id_5.choices[0]
        rangordnungstest.proben_id_3.default = rangordnungstest.proben_id_5.choices[0]
        rangordnungstest.proben_id_4.default = rangordnungstest.proben_id_5.choices[0]
        rangordnungstest.proben_id_5.default = rangordnungstest.proben_id_5.choices[0]

        form.question_types[0].data["submit"] = False
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



@app.route('/training_page/<training>', methods=['GET', 'POST'])
def training_page(training):
    '''
    This function handles the training page for a selected training.
    If the user is not logged in, they are redirected to the login page.
    '''
    if 'username' not in session:
        return redirect(url_for('login'))

    questions = get_questions(training)
    if request.method == 'POST':
        # Handle the user's answer
        answer = request.form.get('answer')
        # TODO: Handle the user's answer
        # ...

        # Get the next question
        current_question_index = request.form.get('current_question_index')
        current_question_index=int(current_question_index)
        print(current_question_index + 1 < len(questions))
        if current_question_index + 1 < len(questions):
            next_question = questions[current_question_index + 1]
            return render_template('training_page.html', training=training, question=next_question, current_question_index=current_question_index+1)
        else:
            # TODO: Handle end of questions
            # ...
            pass

    # Render the first question
    questions = Trainings.query.get(training)
    for question in questions:
        if question:
            question_type = ""
    return render_template('training_page.html', training=training, question=questions[0], current_question_index=0)



@app.route('/training_progress/<question>')
def training_progress(question):
    
    return render_template('training_progress.html', question=question)

@app.route('/')
def dashboard():
    """
    This function handles the main dashboard page.
    """
    return render_template('dashboard.html')

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