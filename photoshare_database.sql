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
(1, 'John', 'Doe', 'johndoe@email.com', '1990-01-01', '$2b$12$EQodrXwyfo/5y/LKUedoOOVYMLr1OofuzIan933g2DYeEiANEyklO', 'male', 'New York'),
(2, 'Jane', 'Doe', 'janedoe@email.com', '1995-02-15', '$2b$12$uC6SxBIt54NKuYYR/f1L3umb2QLu4Z6wzh6YVKdT/Jt6ixPHNwvPe', 'female', 'Los Angeles'),
(3, 'Bob', 'Smith', 'bobsmith@email.com', '1985-07-20', '$2b$12$ZIruXTIE8Qutt4P3/B3DueGlwnWNg8KGy2ZW1/SZUuePOfFz0p.ea', 'male', 'Chicago'),
(4, 'Evan', 'Paul', 'epaul@email.com', '2000-05-01', '$2b$12$Prym.bIdlKfHWDKJ9v/VgOOTrH6cLRoYrTMtPlbuqQso/xG8e7Xr.', 'male', 'Phoenix'),
(5, 'Chris', 'Field', 'cfield@email.com', '2005-03-15', '$2b$12$IK4.kMJzxoA6UvvHe/RN..uS5bBePHUfe1YCWY5QZA3K0ZNVKvZyq', 'male', 'Sandwich'),
(6, 'Joe', 'Smith', 'joesmith@email.com', '2009-09-20', '$2b$12$qu7q2QlVefTe7gTlBqqcQ.3N80rwyx.Asy8CAZqzT1lx0ku.nJCWS', 'male', 'Seattle');

INSERT INTO Friends (user1Id, user2Id, date)
VALUES
(1, 2, '2023-01-01'),
(1, 3, '2023-02-15'),
(2, 3, '2023-03-20'),
(1, 4, '2023-04-20'),
(2, 5, '2023-05-01');

INSERT INTO Albums (albumId, userId, name, creationDate)
VALUES
(1, 1, 'user1album1', '2023-04-20'),
(2, 1, 'user1album2', '2023-04-20'),
(3, 2, 'user2album1', '2023-04-20'),
(4, 2, 'user2album2', '2023-04-20'),
(5, 2, 'user2album3', '2023-04-20'),
(6, 3, 'user3album1', '2023-04-20'),
(7, 4, 'user4album1', '2023-04-20'),
(8, 4, 'user4album2', '2023-04-20'),
(9, 5, 'user5album1', '2023-04-20'),
(10, 6, 'user6album1', '2023-04-20'),
(11, 6, 'user6album2', '2023-04-20');

INSERT INTO Photos (photoId, albumId, userId, date, caption)
VALUES
(1, 1, 1, '2023-04-20', 'Test caption'),
(2, 1, 1, '2023-04-20', 'Test caption 2'),
(3, 2, 1, '2023-04-20', 'Test caption 3'),
(4, 3, 2, '2023-04-20', 'Test caption 4'),
(5, 4, 2, '2023-04-20', 'Test caption 5'),
(6, 5, 2, '2023-04-20', 'Test caption 6'),
(7, 6, 3, '2023-04-20', 'Test caption 7'),
(8, 6, 3, '2023-04-20', 'Test caption 8'),
(9, 6, 3, '2023-04-20', 'Test caption 9'),
(10, 7, 4, '2023-04-20', 'Test caption 10'),
(11, 8, 4, '2023-04-20', 'Test caption 11'),
(12, 8, 4, '2023-04-20', 'Test caption 12'),
(13, 9, 5, '2023-04-20', 'Test caption 13'),
(14, 9, 5, '2023-04-20', 'Test caption 14'),
(15, 9, 5, '2023-04-20', 'Test caption 15'),
(16, 10, 6, '2023-04-20', 'Test caption 16'),
(17, 11, 6, '2023-04-20', 'Test caption 17'),
(18, 11, 6, '2023-04-20', 'Test caption 18');

INSERT INTO Tags (photoId, description)
VALUES
(1, 'testing'),
(1, 'the'),
(1, 'tags'),
(2, 'feature'),
(2, 'on'),
(2, 'this'),
(3, 'social'),
(3, 'media'),
(3, 'app'),
(4, 'currently'),
(4, 'in'),
(4, 'development'),
(5, 'named'),
(5, 'photoshare'),
(5, 'at'),
(6, 'the'),
(6, 'moment'),
(6, 'I'),
(7, 'Have'),
(7, 'a'),
(7, 'water'),
(8, 'bottle'),
(8, 'on'),
(8, 'my'),
(9, 'desk'),
(9, 'lasagna'),
(9, 'pizza'),
(10, 'food'),
(10, 'bags'),
(10, 'remote'),
(11, 'lid'),
(11, 'monitor'),
(11, 'keyboard'),
(12, 'mouse'),
(12, 'io'),
(12, 'computer'),
(13, 'database'),
(13, 'cable'),
(13, 'internet'),
(14, 'tech'),
(14, 'stuff'),
(14, 'popular'),
(15, 'popular'),
(15, 'stuff'),
(15, 'popcorn'),
(16, 'popular'),
(16, 'stuff'),
(16, 'popcorn'),
(17, 'popular'),
(17, 'app'),
(17, 'database'),
(18, 'testing'),
(18, 'popular'),
(18, 'mysql');
