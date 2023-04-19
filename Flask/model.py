from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class multiplechoicequestions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=True)
    option4 = db.Column(db.String(255), nullable=True)
    answer = db.Column(db.String(255), nullable=False)
    #training = db.Column(db.String(255), nullable=False)



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
    