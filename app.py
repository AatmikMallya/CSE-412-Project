from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import quoted_name
from sqlalchemy import Column, Integer, String, Date, func, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
import datetime
import os
from pathlib import Path


app = Flask(__name__, template_folder='Templates', static_folder='albums')
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

class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user1Id = db.Column(db.Integer, nullable=False)
    user2Id = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.date.today())

class Albums(db.Model):
    albumId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userId = db.Column(db.Integer, db.ForeignKey('Users.userId'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    creationDate = db.Column(db.Date, nullable=False)
    photos = db.relationship('Photos', backref='album', cascade='all, delete-orphan', primaryjoin="Albums.albumId == Photos.albumId")

class Photos(db.Model):
    photoId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    albumId = db.Column(db.Integer, db.ForeignKey('albums.albumId'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('Users.userId'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    caption = db.Column(db.String(255))
    tags = db.relationship('Tags', backref='photo')

class Tags(db.Model):
    photoId = db.Column(db.Integer, db.ForeignKey('photos.photoId'), primary_key=True)
    description = db.Column(db.String(255))


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
    email = request.args.get('email')
    friends = get_friends(email)
    rec_friends = get_friend_recs(email)
    albums, album_photos = get_user_albums(email)
    print(album_photos)
    return render_template('profile.html', email=email, friends=friends, rec_friends=rec_friends, albums=albums, album_photos=album_photos)



#######################################
#  Actions
#######################################

# Register user
@app.route('/register', methods=['POST'])
def register():
    # Get data from request
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    email = request.form['email']
    dateOfBirth = request.form['dateOfBirth']
    hometown = request.form['hometown']
    gender = request.form['gender']
    password = request.form['password']

    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return render_template('register.html', error='Email already exists')

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
    print(user)
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

@app.route('/upload_album', methods=['POST'])
def upload_album():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    # Get the form data from the request
    album_name = request.form.get('album_name')
    file = request.files['photo']
    tags = request.form.get('tags')

    # Check if the file was uploaded
    if 'photo' not in request.files:
        return 'No file uploaded', 400

    # Check if the file has a filename
    if file.filename == '':
        return 'No file selected', 400

    # Save the file to a temporary location
    # file.save('/tmp/' + file.filename)

    # Create a new Album object
    album = Albums(userId=user.userId, name=album_name, creationDate=datetime.date.today())
    db.session.add(album)
    db.session.commit()

    # Create a new Photo object
    photo = Photos(albumId=album.albumId, userId=user.userId, date=datetime.date.today(), caption=album_name)
    db.session.add(photo)
    db.session.commit()

    # Create Tag objects if tags are provided
    if tags:
        tags_list = tags.split(' ')
        for tag in tags_list:
            tag_obj = Tags(photoId=photo.photoId, description=tag.strip())
            db.session.add(tag_obj)
        db.session.commit()

    # Create a folder for the album with the albumId as the name
    album_folder = Path('albums') / str(album.albumId)
    album_folder.mkdir(parents=True, exist_ok=True)

    # Save the file to the album folder with the photoId as the filename
    file_path = album_folder / f"{photo.photoId}_{file.filename}"
    file.save(file_path)

    # Return a success message
    return 'Album uploaded successfully', 200

# Add friends to the databse
@app.route('/add_friend', methods=['POST'])
def add_friend():
    email = request.form.get('email')
    friend_email = request.form.get('friend_email')

    user =  User.query.filter_by(email=email).first()
    friend = User.query.filter_by(email=friend_email).first()

    if not friend:
        return render_template(f'profile.html', email=email, friend_error='User does not exist')
    
    friendship = Friends(user1Id=user.userId, user2Id=friend.userId)
    db.session.add(friendship)
    db.session.commit()

    return render_template(f'profile.html', email=email, friend_success='Friend added!')

# Return albums for a given user
def get_user_albums(email):
    user = User.query.filter_by(email=email).first()
    albums = Albums.query.filter_by(userId=user.userId).all()

    album_photos = {}
    for album in albums:
        album_path = Path('albums') / str(album.albumId)
        photos = []
        for file_path in album_path.glob('*'):
            if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                photo_id = file_path.stem.split('_')[0]
                photo_path = str(file_path.relative_to('albums'))
                photo_path = photo_path.replace('//', '/')
                photo_path = photo_path.replace('\\\\', '/')
                photos.append((photo_id, photo_path))
        album_photos[album.albumId] = photos

    return albums, album_photos

def get_friends(email):
    user = User.query.filter_by(email=email).first()

    query = text('''SELECT Users.userId, Users.firstName, Users.lastName
                    FROM Users
                    INNER JOIN Friends
                    ON Users.userId = Friends.user2Id
                    WHERE Friends.user1Id = :userId;
                ''')
    params = {"userId": user.userId}
    result = db.session.execute(query, params)
    friends = [User.query.get(user_id[0]) for user_id in result.fetchall()]
    return friends

def get_friend_recs(email):
    user = User.query.filter_by(email=email).first()

    query = text('''SELECT DISTINCT friends2.user2Id FROM Friends friends1
                JOIN Friends friends2 ON friends1.user2Id = friends2.user1Id
                WHERE friends1.user1Id = :userId
                AND friends2.user2Id NOT IN (SELECT user2Id FROM Friends WHERE user1Id = :userId)
                ''')
    params = {"userId": user.userId}
    result = db.session.execute(query, params)
    friend_recs = [User.query.get(user_id[0]) for user_id in result.fetchall()]
    return friend_recs


if __name__ == '__main__':
    app.run(debug=True)



