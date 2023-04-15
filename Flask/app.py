from flask import Flask, render_template, request, session, redirect, url_for ,flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/testdb'
app.config['SECRET_KEY'] = 'secret_key'
db = SQLAlchemy(app)

class Users(db.Model):
    """
    This class represents the Users table in the database.

    Attributes:
        id (int): The id of the user.
        username (str): The username of the user.
        password (str): The password of the user.
        user_type (bool): The type of the user, either a professor or a student.
        training (str): The training that the student is currently assigned to.
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    user_type = db.Column(db.Boolean())
    training = db.Column(db.String(20))
    
    def __repr__(self):
        """
        Returns the username of the user.
        """
        return f"User('{self.username}')"
class multiplechoicequestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=True)
    option4 = db.Column(db.String(255), nullable=True)
    answer = db.Column(db.String(255), nullable=False)
    #training = db.Column(db.String(255), nullable=False)

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
        user = Users.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            return redirect(url_for('professor_dashboard'))
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
        
        
        new_user = Users(username=username, password=password, user_type=False)
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
        user = Users.query.filter_by(username=username).first()
        if user.user_type == False:
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
        user = Users.query.filter_by(username=username).first()
        if user.user_type == True:
            trainings = ['Training 1', 'Training 2', 'Training 3'] # Example list of available trainings TODO: LIST
            return render_template('professor_dashboard.html', trainings=trainings)
        elif user.user_type == False:
            return redirect(url_for('student_waitingroom'))
    return redirect(url_for('login'))


@app.route('/select_training/<training>')
def select_training(training):
    """
    This function handles the selection of a training by a professor.
    It sets the 'training' attribute of all students to the selected training.
    After updating the database, it redirects to the training page for the selected training.
    """
    students = Users.query.filter_by(user_type=False).all()
    for student in students:
        student.training = training
        db.session.commit()
    return redirect(url_for('training_progress', question =get_questions(training)))                                  



@app.route('/training_page/<training>')
def training_page(training):
    """
    This function handles the training page for a selected training.
    If the user is not logged in, they are redirected to the login page.
    """
    if 'username' in session:
        question = get_questions(training)
        return render_template('training_page.html', question=question)
    else:
        return redirect(url_for('login'))


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
    questions = multiplechoicequestions.query.all()
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

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    id = int(request.form['id'])
    answer = request.form['answer']
    is_correct = answer == questions[id-1]['answer']
    if is_correct and id < len(questions):
        next_question = questions[id]
    else:
        next_question = {'id': None}
    return jsonify(next_question)

if __name__ == '__main__':
    app.run(debug=True)