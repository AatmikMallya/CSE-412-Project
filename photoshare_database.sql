DROP DATABASE IF EXISTS `photoshare_database`;
CREATE DATABASE `photoshare_database`; 
USE `photoshare_database`;

CREATE TABLE Users (
    userId INTEGER PRIMARY KEY,
    firstName TEXT,
    lastName TEXT,
    email VARCHAR(255) UNIQUE,
    dateOfBirth DATE,
    password TEXT,
    gender TEXT,
    hometown TEXT
);

CREATE TABLE Friends (
    user1Id INTEGER,
    user2Id INTEGER,
    date DATE,
    FOREIGN KEY (user1Id) REFERENCES Users(userId),
    FOREIGN KEY (user2Id) REFERENCES Users(userId)
);

CREATE TABLE Albums (
    albumId INTEGER PRIMARY KEY AUTO_INCREMENT,
    userId INTEGER,
    name TEXT,
    creationDate DATE,
    FOREIGN KEY (userId) REFERENCES Users(userId)
);

CREATE TABLE Photos (
    photoId INT PRIMARY KEY AUTO_INCREMENT,
    albumId INT,
    userId INT,
    date DATE,
    caption TEXT,
    FOREIGN KEY (albumId) REFERENCES Albums(albumId) ON DELETE CASCADE,
    FOREIGN KEY (userId) REFERENCES Users(userId)
);

CREATE TABLE Tags (
    photoId INTEGER,
    description TEXT,
    FOREIGN KEY (photoId) REFERENCES Photos (photoId) ON DELETE CASCADE
);

CREATE TABLE Likes (
  photoId INT,
  userId INT,
  FOREIGN KEY (photoId) REFERENCES Photos (photoId) ON DELETE CASCADE,
  FOREIGN KEY (userId) REFERENCES Users (userId)
);

CREATE TABLE Comments (
  commentId INT PRIMARY KEY AUTO_INCREMENT,
  photoId INT,
  userId INT,
  text TEXT,
  date DATE,
  FOREIGN KEY (photoId) REFERENCES Photos (photoId) ON DELETE CASCADE,
  FOREIGN KEY (userId) REFERENCES Users (userId)
);

INSERT INTO Users (userId, firstName, lastName, email, dateOfBirth, password, gender, hometown)
VALUES
(1, 'John', 'Doe', 'johndoe@email.com', '1990-01-01', 'password', 'male', 'New York'),
(2, 'Jane', 'Doe', 'janedoe@email.com', '1995-02-15', 'password123', 'female', 'Los Angeles'),
(3, 'Bob', 'Smith', 'bobsmith@email.com', '1985-07-20', 'password456', 'male', 'Chicago'),
(4, 'Evan', 'Paul', 'epaul@email.com', '2000-05-01', 'password789', 'male', 'Phoenix'),
(5, 'Chris', 'Field', 'cfield@email.com', '2005-03-15', 'password321', 'male', 'Sandwich'),
(6, 'Joe', 'Smith', 'joesmith@email.com', '2009-09-20', 'password654', 'male', 'Seattle');

INSERT INTO Friends (user1Id, user2Id, date)
VALUES
(1, 2, '2023-01-01'),
(1, 3, '2023-02-15'),
(2, 3, '2023-03-20'),
(1, 4, '2023-04-20'),
(2, 5, '2023-05-01');
