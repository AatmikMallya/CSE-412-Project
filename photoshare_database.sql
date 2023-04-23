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
(6, 'Joe', 'Smith', 'joesmith@email.com', '2009-09-20', '$2b$12$qu7q2QlVefTe7gTlBqqcQ.3N80rwyx.Asy8CAZqzT1lx0ku.nJCWS', 'male', 'Seattle'),
(7, 'Kimberly', 'Griffith', 'caleigh.koc2@hotmail.com', '1992-01-21', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAeAAO7.5O1XRSVbRTG5F9x/Jt7MRiJirC', 'female', 'Chicago'),
(8, 'Mary', 'Lanigan', 'pink1995@yahoo.com', '1995-02-15', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAev7rSu5Am/x0aMH1ecxpLsYa5IauTRhS', 'female', 'Seal Beach'),
(9, 'Karen', 'Brown', 'aliya.yos1@gmail.com', '1987-06-27', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAeyeiz7jo10AThhvc4HU0XvFDAhL7S2eu', 'female', 'Washington'),
(10, 'Elvis', 'Ladner', 'erika_brau0@yahoo.com', '1983-11-04', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAeF7GS940JIBfApm.5NSCJ.mKb.avhcLy', 'male', 'Omaha'),
(11, 'Michael', 'Ramos', 'alice_colli@yahoo.com', '1994-11-26', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAejNZNUPGQAZeYFqm1CbuRSr2PMg7ihUC', 'male', 'Sandusky'),
(12, 'Christopher', 'Neubauer', 'shyanne2002@yahoo.com', '1982-05-27', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAehOSf5UpxXv7yDa3EGcEFk2pL9eK4q.i', 'male', 'Los Alamos'),
(13, 'Daisy', 'Monger', 'lourdes2007@yahoo.com', '1985-07-13', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAebzloUzmSg.te71mwv3TvDz662BX/2WG', 'female', 'Wausau'),
(14, 'Jill', 'Plumb', 'loma2017@gmail.com', '1964-07-20', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAeEmbg1xLhA.kAm5RwBJAi7ZcnetprdmS', 'female', 'Mellette'),
(15, 'Judith', 'Grimsley', 'juliet1998@hotmail.com', '1990-05-10', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAeDp7IxXijk2IBPPm8o1QiLyCU/y7tFsO', 'female', 'Dewitt'),
(16, 'Donald', 'Devine', 'luisa2001@yahoo.com', '1998-11-16', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAewDrlbW8wOXYmMnFx8UX8dpIIVffdgtW', 'male', 'New Martinsville'),
(17, 'James', 'Smallwood', 'deborah2011@hotmail.com', '1970-09-19', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAeHa.ZRlXe2Omio3KKL1vl/B5eyHQeWWy', 'male', 'Philadelphia'),
(18, 'Judy', 'Ochoa', 'moses.leann@gmail.com', '1957-12-11', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAe1l5pnRfug7SR2EFxD3b3gdbIqAFGPUK', 'female', 'Boston'),
(19, 'George', 'Huffman', 'keyshawn1975@yahoo.com', '1990-05-12', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAe6PGL7jgRh3SIC76KQ9RcCI1Jg9nTtpu', 'male', 'Champaign'),
(20, 'Tyrone', 'Cordero', 'abbey.welc2@yahoo.com', '1978-10-07', '$2b$12$Q6fEDU6RrK6rOy6Cq3zqAehiEts71mkjufuUpRurLOoLY3sk/WvPa', 'male', 'Sacramento');

INSERT INTO Friends (user1Id, user2Id, date)
VALUES
(1, 2, '2023-01-01'),
(1, 3, '2023-02-15'),
(2, 3, '2023-03-20'),
(1, 4, '2023-04-20'),
(2, 5, '2023-05-01'),
(1, 6, '2023-04-22'),
(6, 12, '2023-04-23'),
(6, 16, '2023-02-15'),
(8, 11, '2023-03-20'),
(9, 15, '2023-04-23'),
(10, 19, '2023-06-01'),
(20, 10, '2023-03-18');

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

INSERT INTO Likes(photoId, userId)
VALUES
(1,2),
(1,3),
(1,4),
(2,2),
(2,3),
(2,5),
(3,2),
(4,1),
(4,3),
(4,6),
(5,1),
(6,1),
(6,3),
(6,6),
(7,1),
(7,2),
(7,4),
(7,5),
(7,6),
(8,1),
(8,2),
(9,6),
(10,1),
(10,2),
(10,3),
(11,1),
(11,2),
(12,1),
(12,2),
(13,1),
(13,2),
(13,3),
(13,4),
(14,1),
(14,2),
(15,1),
(16,1),
(16,2),
(16,3),
(16,4),
(16,5),
(17,1),
(17,2),
(18,1),
(18,2),
(18,3),
(18,4),
(18,5);

INSERT INTO Comments(commentId, photoId, userId, text, date)
VALUES
(1,1,2,'this is test comment #1','2023-04-20'),
(2,1,3,'this is test comment #2','2023-04-20'),
(3,1,4,'this is test comment #3','2023-04-20'),
(4,2,2,'this is test comment #4','2023-04-20'),
(5,2,3,'this is test comment #5','2023-04-20'),
(6,2,5,'this is test comment #6','2023-04-20'),
(7,3,2,'this is test comment #7','2023-04-20'),
(8,4,1,'this is test comment #8','2023-04-20'),
(9,4,3,'this is test comment #9','2023-04-20'),
(10,4,6,'this is test comment #10','2023-04-20'),
(11,5,1,'this is test comment #11','2023-04-20'),
(12,6,1,'this is test comment #12','2023-04-20'),
(13,6,3,'this is test comment #13','2023-04-20'),
(14,6,6,'this is test comment #14','2023-04-20'),
(15,7,1,'this is test comment #15','2023-04-20'),
(16,7,2,'this is test comment #16','2023-04-20'),
(17,7,4,'this is test comment #17','2023-04-20'),
(18,7,5,'this is test comment #18','2023-04-20'),
(19,7,6,'this is test comment #19','2023-04-20'),
(20,8,1,'this is test comment #20','2023-04-20'),
(21,8,2,'this is test comment #21','2023-04-20'),
(22,9,6,'this is test comment #22','2023-04-20'),
(23,10,1,'this is test comment #23','2023-04-20'),
(24,10,2,'this is test comment #24','2023-04-20'),
(25,10,3,'this is test comment #25','2023-04-20'),
(26,11,1,'this is test comment #26','2023-04-20'),
(27,11,2,'this is test comment #27','2023-04-20'),
(28,12,1,'this is test comment #28','2023-04-20'),
(29,12,2,'this is test comment #29','2023-04-20'),
(30,13,1,'this is test comment #30','2023-04-20'),
(31,13,2,'this is test comment #31','2023-04-20'),
(32,13,3,'this is test comment #32','2023-04-20'),
(33,13,4,'this is test comment #33','2023-04-20'),
(34,14,1,'this is test comment #34','2023-04-20'),
(35,14,2,'this is test comment #35','2023-04-20'),
(36,15,1,'this is test comment #36','2023-04-20'),
(37,16,1,'this is test comment #37','2023-04-20'),
(38,16,2,'this is test comment #38','2023-04-20'),
(39,16,3,'this is test comment #39','2023-04-20'),
(40,16,4,'this is test comment #40','2023-04-20'),
(41,16,5,'this is test comment #41','2023-04-20'),
(42,17,1,'this is test comment #42','2023-04-20'),
(43,17,2,'this is test comment #43','2023-04-20'),
(44,18,1,'this is test comment #44','2023-04-20'),
(45,18,2,'this is test comment #45','2023-04-20'),
(46,18,3,'this is test comment #46','2023-04-20'),
(47,18,4,'this is test comment #47','2023-04-20'),
(48,18,5,'this is test comment #48','2023-04-20');
