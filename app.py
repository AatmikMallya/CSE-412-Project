from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import quoted_name, text
from sqlalchemy import Column, Integer, String, Date, func, text, cast, desc, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
import datetime
import os
from pathlib import Path
import glob

app = Flask(__name__, template_folder='Templates', static_folder='albums')
app.secret_key = 'your_secret_key_here'
bcrypt = Bcrypt(app)

# Configure MySQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/photoshare_database' # Replace with your MySQL database connection details
db = SQLAlchemy(app)
with app.app_context():
    db.session.execute(text("SET sql_mode=(SELECT REPLACE(@@sql_mode,'ONLY_FULL_GROUP_BY',''));"))

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
    __tablename__ = 'photos'
    photoId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    albumId = db.Column(db.Integer, db.ForeignKey('albums.albumId'), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey('Users.userId'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    caption = db.Column(db.String(255))
    tags = db.relationship('Tags', backref='photo', cascade='all, delete-orphan', passive_deletes=True)

class Tags(db.Model):
    photoId = db.Column(db.Integer, db.ForeignKey('photos.photoId', ondelete='CASCADE'), primary_key=True)
    description = db.Column(db.String(255))

class Likes(db.Model):
    photoId = db.Column(db.Integer, db.ForeignKey('photos.photoId', ondelete='CASCADE'), primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('Users.userId'), primary_key=True)

class Comments(db.Model):
    commentId = db.Column(db.Integer, primary_key=True)
    photoId = db.Column(db.Integer, db.ForeignKey('photos.photoId', ondelete='CASCADE'))
    userId = db.Column(db.Integer, db.ForeignKey('Users.userId'))
    text = db.Column(db.Text)
    date = db.Column(db.Date)


#######################################
#  Render html pages
#######################################
@app.route('/', methods=['GET','POST'])
@app.route('/index.html', methods=['GET','POST'])
def home_page(tag=None):
    tag = request.args.get('tag')
    search_results = None
    if tag:
            search_results = search_photos_by_tags(tag)
    if request.method == 'POST':
        tags = request.form['tags']
        search_results = search_photos_by_tags(tags)
    popular_tags = get_most_popular_tags()
    top_users = top_contributors()
    album_users, album_photos = get_all_albums()
    if 'user_email' in session:
        email = session['user_email']
        return render_template('index.html', email=email, album_users=album_users, album_photos=album_photos, top_users=top_users, search_results=search_results, popular_tags=popular_tags)
    return render_template('index.html', album_users=album_users, album_photos=album_photos, top_users=top_users, search_results=search_results, popular_tags=popular_tags)

@app.route('/register.html', methods=['GET'])
def register_page():
    min_dob = datetime.datetime.now() - datetime.timedelta(days=13 * 365)
    min_dob_str = min_dob.date().isoformat()
    return render_template('register.html', min_dob=min_dob_str)

@app.route('/profile.html', methods=['GET'])
def profile_page():
    email = request.args.get('email')
    friends = get_friends(email)
    rec_friends = get_friend_recs(email)
    albums, album_photos = get_user_albums(email)
    recommended_photos = you_may_also_like(email)
    print(album_photos)
    return render_template('profile.html', email=email, friends=friends, rec_friends=rec_friends, albums=albums, album_photos=album_photos, recommended_photos=recommended_photos)



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
    session['user_email'] = email
    return redirect(url_for('home_page', email=email))

@app.route('/search_comments', methods=['POST'])
def search_comments():
    query = request.form['comment_search']
    query_string = text("""
    SELECT 
        Users.userId, Users.firstName, Users.lastName, COUNT(*) as matching_comments_count
    FROM
        Users
    JOIN
        Comments ON Users.userId = Comments.userId
    WHERE
        Comments.text LIKE :query
    GROUP BY
        Users.userId
    ORDER BY
        matching_comments_count DESC;
    """)

    # Execute the query with the search query parameter
    users_with_matching_comments = db.session.execute(query_string, {'query': f'%{query}%'}).fetchall()
    popular_tags = get_most_popular_tags()
    top_users = top_contributors()
    album_users, album_photos = get_all_albums()
    if 'user_email' in session:
        email = session['user_email']
        return render_template('index.html', email=email, album_users=album_users, album_photos=album_photos, top_users=top_users, search_results=None, popular_tags=popular_tags,users_with_matching_comments=users_with_matching_comments)
    return render_template('index.html', album_users=album_users, album_photos=album_photos, top_users=top_users, search_results=None, popular_tags=popular_tags,users_with_matching_comments=users_with_matching_comments)

# Logout route
@app.route('/logout')
def logout():
    # Clear session data
    session.pop('user_email', None)
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
    caption = request.form.get('caption')

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
    photo = Photos(albumId=album.albumId, userId=user.userId, date=datetime.date.today(), caption=caption)
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

@app.route('/albums/<int:album_id>/add_photo', methods=['POST'])
def add_photo(album_id):
    album = Albums.query.get_or_404(album_id)
    file = request.files['photo']
    tags = request.form.get('tags')
    caption = request.form.get('caption')
    email = request.form.get('email')

    if file:
        photo = Photos(albumId=album.albumId, userId=album.userId, date=datetime.date.today(), caption=caption)
        db.session.add(photo)
        db.session.commit()

        if tags:
            tags_list = tags.split(' ')
            for tag in tags_list:
                tag_obj = Tags(photoId=photo.photoId, description=tag.strip())
                db.session.add(tag_obj)
            db.session.commit()

        # Save the file to the album folder with the photoId as the filename
        album_folder = Path('albums') / str(album.albumId)

        # Save the file to the album folder with the photoId as the filename
        file_path = album_folder / f"{photo.photoId}_{file.filename}"
        file.save(file_path)

        return redirect(url_for('profile_page', email=email) )
    else:
        flash('No file selected.', 'error')
        return redirect(url_for('profile_page', email=email) )

@app.route('/albums/<int:album_id>/delete_photo/<int:photo_id>', methods=['POST'])
def delete_photo(album_id, photo_id):
    email = request.form.get('email')
    photo = Photos.query.filter_by(photoId=photo_id, albumId=album_id).first()
    if not photo:
        flash('Photo not found', 'error')
        return redirect(url_for('album', album_id=album_id, email=session['email']))
    # Delete the photo from the file system
    photo_path = Path('albums') / str(photo.albumId)
    
    # photo_path.unlink()
    # Delete the selected files
    for file_path in photo_path.glob(f'{photo.photoId}*'):
        file_path.unlink()

    # Delete the photo from the database
    db.session.delete(photo)
    db.session.commit()
    flash('Photo deleted successfully', 'success')
    return redirect(url_for('profile_page', email=email) )

@app.route('/like_photo', methods=['POST'])
def like_photo():
    photo_id = request.form.get('photo_id')
    email = request.form.get('email')
    user_id =  User.query.filter_by(email=email).first().userId
    like = Likes.query.filter_by(photoId=photo_id, userId=user_id).first()

    if like:
        # Unlike the photo
        db.session.delete(like)
    else:
        # Like the photo
        new_like = Likes(photoId=photo_id, userId=user_id)
        db.session.add(new_like)

    db.session.commit()

    return redirect('index.html')

@app.route('/add_comment', methods=['POST'])
def add_comment():
    photo_id = request.form.get('photo_id')
    email = request.form.get('email')
    user_id =  User.query.filter_by(email=email).first().userId
    text = request.form.get('text')
    new_comment = Comments(photoId=photo_id, userId=user_id, text=text, date=datetime.date.today())
    db.session.add(new_comment)
    db.session.commit()

    return redirect('index.html')

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

def you_may_also_like(email):
    user = User.query.filter_by(email=email).first()
    top_tags = get_top_tags_for_user(user.userId)
    recommended_photos = get_recommended_photos(user.userId, top_tags)
    print('bbbbbb',recommended_photos)
    return recommended_photos

def get_top_tags_for_user(user_id, limit=5):
    top_tags = db.session.query(Tags.description, func.count(Tags.description)).\
        join(Photos, Photos.photoId == Tags.photoId).\
        filter(Photos.userId == user_id).\
        group_by(Tags.description).\
        order_by(func.count(Tags.description).desc()).\
        limit(limit).all()
    return [tag for tag, count in top_tags]

def get_recommended_photos(user_id, top_tags):
    if not top_tags:  # Check if top_tags is empty
        return []
    # Use the updated SQL query with GROUP_CONCAT
    query = text("""
    SELECT 
        photos.`photoId` AS `photos_photoId`,
        photos.`albumId` AS `photos_albumId`,
        photos.`userId` AS `photos_userId`,
        photos.date AS photos_date,
        photos.caption AS photos_caption,
        `Users`.`userId` AS `Users_userId`,
        `Users`.`firstName` AS `Users_firstName`,
        `Users`.`lastName` AS `Users_lastName`,
        `Users`.email AS `Users_email`,
        `Users`.`dateOfBirth` AS `Users_dateOfBirth`,
        `Users`.hometown AS `Users_hometown`,
        `Users`.gender AS `Users_gender`,
        `Users`.password AS `Users_password`,
        GROUP_CONCAT(DISTINCT tags.description) AS tags_description,
        COUNT(DISTINCT likes.`userId`) AS likes_count,
        COUNT(DISTINCT comments.`commentId`) AS comments_count,
        SUM(tags.description IN :top_tags AND photos.`userId` != :userId_1) AS score
    FROM photos
    INNER JOIN tags ON tags.`photoId` = photos.`photoId`
    INNER JOIN `Users` ON `Users`.`userId` = photos.`userId`
    LEFT OUTER JOIN likes ON likes.`photoId` = photos.`photoId`
    LEFT OUTER JOIN comments ON comments.`photoId` = photos.`photoId`
    WHERE photos.`userId` != :userId_1
    GROUP BY photos.`photoId`, `Users`.`userId`
    ORDER BY score DESC
        """)

    # Execute the query with the user_id and top_tags parameters
    recommended_photos = db.session.execute(query, {'userId_1': user_id, 'top_tags': top_tags}).fetchall()

    results = []
    for row in recommended_photos:
        (
            photos_photoId, photos_albumId, photos_userId, photos_date,
            photos_caption, Users_userId, Users_firstName, Users_lastName,
            Users_email, Users_dateOfBirth, Users_hometown, Users_gender,
            Users_password, tags_description, likes_count, comments_count, score
        ) = row  # Unpack the row with the correct number of values
        album_path = Path('albums') / str(photos_albumId)
        
        photo_path = None
        for file_path in album_path.glob(f'{photos_photoId}*'):
            if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                photo_path = str(file_path.relative_to('albums'))
                photo_path = photo_path.replace('//', '/')
                photo_path = photo_path.replace('\\\\', '/')
                break
        
        if photo_path:
            photo = Photos(
                photoId=photos_photoId,
                albumId=photos_albumId,
                userId=photos_userId,
                date=photos_date,
                caption=photos_caption
            )
            
            user = User(
                userId=Users_userId,
                firstName=Users_firstName,
                lastName=Users_lastName,
                email=Users_email,
                dateOfBirth=Users_dateOfBirth,
                hometown=Users_hometown,
                gender=Users_gender,
                password=Users_password
            )
            results.append((photo, user, tags_description, score, photo_path, likes_count, comments_count))  # Append the values to the results list

    return results

# Return albums for a given user
def get_user_albums(email):
    print(email)
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
                photo_tags = []
                photo = Photos.query.filter_by(photoId=photo_id, albumId=album.albumId).first()
                if photo:
                    for tag in photo.tags:
                        photo_tags.append(tag.description)
                like_count = Likes.query.filter_by(photoId=photo_id).count()
                likes = Likes.query.filter_by(photoId=photo_id).all()
                likers = [User.query.filter_by(userId=like.userId).first() for like in likes]
                like_count = len(likes)
                comments = []
                for comment in Comments.query.filter_by(photoId=photo.photoId).all():
                    author = User.query.filter_by(userId=comment.userId).first()
                    comments.append((comment, author))
                photos.append((photo_id, photo_path, photo_tags, photo, like_count, comments, likers))
        album_photos[album.albumId] = photos

    return albums, album_photos

def get_all_albums():
    album_users = db.session.query(Albums, User).join(User, Albums.userId == User.userId).all()
    album_photos = {}
    
    for album, user in album_users:
        album_path = Path('albums') / str(album.albumId)
        photos = []
        for file_path in album_path.glob('*'):
            if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                photo_id = file_path.stem.split('_')[0]
                photo_path = str(file_path.relative_to('albums'))
                photo_path = photo_path.replace('//', '/')
                photo_path = photo_path.replace('\\\\', '/')
                photo_tags = []
                photo = Photos.query.filter_by(photoId=photo_id, albumId=album.albumId).first()
                if photo:
                    for tag in Tags.query.filter_by(photoId=photo.photoId).all():
                        photo_tags.append(tag.description)
                like_count = Likes.query.filter_by(photoId=photo_id).count()
                likes = Likes.query.filter_by(photoId=photo_id).all()
                likers = [User.query.filter_by(userId=like.userId).first() for like in likes]
                like_count = len(likes)
                comments = []
                for comment in Comments.query.filter_by(photoId=photo.photoId).all():
                    author = User.query.filter_by(userId=comment.userId).first()
                    comments.append((comment, author))
                photos.append((photo_id, photo_path, photo_tags, photo, like_count, comments, likers))
        album_photos[album.albumId] = photos
    print(album_users)
    return album_users, album_photos

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

def top_contributors():
    users = db.session.query(User, func.count(Photos.photoId) + func.count(Comments.commentId)).\
    outerjoin(Photos, User.userId == Photos.userId).\
    outerjoin(Comments, User.userId == Comments.userId).\
    group_by(User.userId).\
    order_by((func.count(Photos.photoId) + func.count(Comments.commentId)).desc()).\
    limit(10).all()
    return users


def search_photos_by_tags(tags):
    tag_list = tags.split()

    subquery = (
        db.session.query(Tags.photoId)
        .filter(Tags.description.in_(tag_list))
        .group_by(Tags.photoId)
        .having(db.func.count(Tags.photoId) == len(tag_list))
        .subquery()
    )

    photos_query = (
        db.session.query(Photos)
        .join(subquery, subquery.c.photoId == Photos.photoId)
    )

    photos = photos_query.all()
    photo_results = []
    for photo in photos:
        album_path = Path('albums') / str(photo.albumId)
        photo_path = None
        for file_path in album_path.glob(f'{photo.photoId}*'):
            if file_path.suffix.lower() in ['.jpg', '.jpeg', '.png']:
                photo_path = str(file_path.relative_to('albums'))
                photo_path = photo_path.replace('//', '/')
                photo_path = photo_path.replace('\\\\', '/')
                break

        photo_tags = [tag.description for tag in photo.tags]
        like_count = Likes.query.filter_by(photoId=photo.photoId).count()
        likes = Likes.query.filter_by(photoId=photo.photoId).all()
        likers = [User.query.filter_by(userId=like.userId).first() for like in likes]

        comments = []
        for comment in Comments.query.filter_by(photoId=photo.photoId).all():
            author = User.query.filter_by(userId=comment.userId).first()
            comments.append((comment, author))

        photo_results.append((photo.photoId, photo_path, photo_tags, photo, like_count, comments, likers))

    return photo_results

def get_most_popular_tags(limit=10):
    popular_tags = (
        db.session.query(Tags.description, db.func.count(Tags.photoId).label("count"))
        .group_by(Tags.description)
        .order_by(db.desc("count"))
        .limit(limit)
    ).all()

    popular_tags = [t[0] for t in popular_tags]

    return popular_tags



if __name__ == '__main__':
    app.run(debug=True)



