from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='Templates')

# Configure MySQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/mydatabase' # Replace with your MySQL database connection details
db = SQLAlchemy(app)

# Define database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    age = db.Column(db.Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age


# Render html pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register.html', methods=['GET'])
def registration_form():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():

    # Get data from request
    first_name = request.form['first-name']
    last_name = request.form['last-name']
    email = request.form['email']
    date_of_birth = request.form['dateofbirth']
    hometown = request.form['hometown']
    gender = request.form['gender']
    password = request.form['password']

    
    # Create a new user object

    # Add the user object to the session and commit to the database
    # db.session.add(new_user)
    # db.session.commit()

    return f'{first_name} registered successfully'


# Login route
@app.route('/login', methods=['POST'])
def login():
    # Get form data
    username = request.form['username']
    password = request.form['password']

    # Query User table to check if username and password match
    user = User.query.filter_by(username=username, password=password).first()

    if user:
        # Successful login
        return f"Welcome, {user.username}!"
    else:
        # Invalid username or password
        return "Invalid username or password. Please try again."





if __name__ == '__main__':
    app.run(debug=True)



# index.html
# register.html
# profile.html


