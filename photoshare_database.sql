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
    albumId INTEGER PRIMARY KEY,
    userId INTEGER,
    name TEXT,
    creationDate DATE,
    FOREIGN KEY (userId) REFERENCES Users(userId)
);

CREATE TABLE Photos (
    photoId INT PRIMARY KEY,
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
  commentId INT PRIMARY KEY,
  photoId INT,
  userId INT,
  text TEXT,
  date DATE,
  FOREIGN KEY (photoId) REFERENCES Photos (photoId) ON DELETE CASCADE,
  FOREIGN KEY (userId) REFERENCES Users (userId)
);
