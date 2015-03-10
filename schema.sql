
CREATE TABLE if not exists users (
  id INTEGER NOT NULL,
  name VARCHAR(50),
  email VARCHAR(120),
  password VARCHAR(100),

  PRIMARY KEY (id),
  UNIQUE (name),
  UNIQUE (email)
);

CREATE TABLE not exists authors (
  id INTEGER NOT NULL,
  name VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE not exists books (
  id INTEGER NOT NULL,
  title VARCHAR(50) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE not exists books_authors (
  fk_book INTEGER,
  fk_author INTEGER,
  FOREIGN KEY(fk_book) REFERENCES books (id),
  FOREIGN KEY(fk_author) REFERENCES authors (id)
);