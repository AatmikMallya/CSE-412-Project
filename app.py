from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import quoted_name
from sqlalchemy import Column, Integer, String, Date, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt

app = Flask(__name__, template_folder='Templates')
app.secret_key = 'your_secret_key_here'
bcrypt = Bcrypt(app)

# Configure MySQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/photoshare_database' # Replace with your MySQL database connection details
db = SQLAlchemy(app)

#######################################
# Define database models
#######################################
class User(db.Model):
    __tablename__ = quoted_name('Users', quote=True)
    userId = Column(Integer, primary_key=True)
    firstName = db.Column(db.String(50), nullable=False)
    lastName = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    dateOfBirth = db.Column(db.String(10), nullable=False)
    hometown = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, userId, firstName, lastName, email, dateOfBirth, hometown, gender, password):
        self.userId = userId
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.dateOfBirth = dateOfBirth
        self.hometown = hometown
        self.gender = gender
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')



#######################################
#  Render html pages
#######################################
@app.route('/')
@app.route('/index.html')
def home_page():
    return render_template('index.html')

@app.route('/register.html', methods=['GET'])
def register_page():
    return render_template('register.html')

@app.route('/profile.html', methods=['GET'])
def profile_page():
    return render_template('profile.html')



#######################################
#  Queries
#######################################

# Register user
@app.route('/register', methods=['POST'])
def register():
    # Get data from request
    print('ASDFASDF', request.form)
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    dateOfBirth = request.form['dateOfBirth']
    hometown = request.form['hometown']
    gender = request.form['gender']
    password = request.form['password']

    # Calculate userId
    max_user_id = db.session.query(func.max(User.userId)).scalar()
    newUserId = max_user_id + 1 if max_user_id else 1
    
    # Create a new User object
    new_user = User(userId=newUserId, firstName=firstName, lastName=lastName, email=email,
                    dateOfBirth=dateOfBirth, hometown=hometown, gender=gender, password=password)

    # Add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return f'{firstName} registered successfully'


# Login route
@app.route('/login', methods=['POST'])
def login():
    # Get form data
    email = request.form['email']
    password = request.form['password']

    # Query User table to check if username and password match
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user:
        if user and bcrypt.check_password_hash(user.password, password):
            session['logged_in'] = True
            session['user_email'] = email
            flash('Login successful', 'success')  # Flash error message
        else:
            flash('Incorrect password', 'error')  # Flash error message
    else:
        flash('User not found', 'error')  # Flash error message
    
    return render_template('index.html', email=email)



# Logout route
@app.route('/logout')
def logout():
    # Clear session data
    session.clear()

    return redirect('index.html')






if __name__ == '__main__':
    app.run(debug=True)



