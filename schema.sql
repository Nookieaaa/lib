DROP TABLE if exists users;
CREATE TABLE users (
  id INTEGER NOT NULL,
  name VARCHAR(50),
  email VARCHAR(120),
  password VARCHAR(100),

  PRIMARY KEY (id),
  UNIQUE (name),
  UNIQUE (email)
);
DROP TABLE if exists authors;
CREATE TABLE authors (
  id INTEGER NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);
DROP TABLE if exists books;
CREATE TABLE books (
  id INTEGER NOT NULL,
  title VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);
DROP TABLE if exists books_authors;
CREATE TABLE books_authors (
  fk_book INTEGER,
  fk_author INTEGER,
  FOREIGN KEY(fk_book) REFERENCES books (id),
  FOREIGN KEY(fk_author) REFERENCES authors (id)
);