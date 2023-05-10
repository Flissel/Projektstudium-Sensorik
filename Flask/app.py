from flask import Flask, render_template, request, session, redirect, url_for ,flash
from flask_sqlalchemy import SQLAlchemy
from model import db, benutzer, Trainings, MultipleChoiceQuestions, CheckboxQuestions, CheckboxGridQuestions, GridQuestions, TextQuestions, ListQuestions


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/praktikum_db'
app.config['SECRET_KEY'] = 'secret_key'
db.init_app(app)

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
        user = benutzer.query.filter_by(benutzername=username).first()

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
        
        
        new_user = benutzer(benutzername=username, passwort=password, rolle=False)
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
        user = benutzer.query.filter_by(benutzername=username).first()
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
        user = benutzer.query.filter_by(benutzername=username).first()
        if user.rolle == True:
            trainings = ['Training 1', 'Training 2', 'Training 3'] # Example list of available trainings TODO: LIST
            return render_template('professor_dashboard.html', trainings=trainings)
        elif user.rolle == False:
            return redirect(url_for('student_waitingroom'))
    return redirect(url_for('login'))

@app.route('/professor_dashboard/create_training')
def create_training():
    """
    This function handles the professor dashboard page.
    If the user is logged in as a professor, they are shown the page with the available trainings.
    If the user is logged in as a student, they are redirected to the student waiting room.
    If the user is not logged in, they are redirected to the login page.
    """
    if 'username' in session:
        username = session['username']
        user = benutzer.query.filter_by(benutzername=username).first()
        if user.rolle == True:
            if request.method == 'POST':
                # Retrieve the form data
                training_name = request.form['training_name']
                selected_question_ids = request.form.getlist('questions[]')

                # Create the new training object
                training = Trainings(name=training_name)
                for i, question_id in enumerate(selected_question_ids):
                    setattr(training, f'multiplechoice_question{i+1}_id', question_id)

                # Add the new training to the database
                db.session.add(training)
                db.session.commit()

                # Redirect to the list of trainings
                return redirect(url_for('professor_dashboard'))

            else:
                # Display the form
                questions = (
                MultipleChoiceQuestions.query
                .with_entities(MultipleChoiceQuestions.multiple_choice_question_id, MultipleChoiceQuestions.question)
                .all()
            )
            questions += (
                CheckboxQuestions.query
                .with_entities(CheckboxQuestions.checkbox_question_id, CheckboxQuestions.question)
                .all()
            )
            questions += (
                CheckboxGridQuestions.query
                .with_entities(CheckboxGridQuestions.checkbox_grid_question_id, CheckboxGridQuestions.question)
                .all()
            )
            questions += (
                GridQuestions.query
                .with_entities(GridQuestions.grid_question_id, GridQuestions.question)
                .all()
            )
            questions += (
                TextQuestions.query
                .with_entities(TextQuestions.text_question_id, TextQuestions.question)
                .all()
            )
            questions += (
                ListQuestions.query
                .with_entities(ListQuestions.list_question_id, ListQuestions.question)
                .all()
            )
            return render_template('create_training.html', questions=questions)
            
                
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
    students = benutzer.query.filter_by(rolle=False).all()
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



      


if __name__ == '__main__':
    app.run(debug=True)