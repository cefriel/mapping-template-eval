USE db;
DROP TABLE IF EXISTS db.student;

CREATE TABLE student (
  ID INTEGER,
  FirstName VARCHAR(50),
  LastName VARCHAR(50)
);
INSERT INTO student values ('10', 'Venus', 'Williams');
