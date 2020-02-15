CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    password VARCHAR NOT NULL
);

CREATE TABLE authors (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL
);

CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn VARCHAR NOT NULL,
    title VARCHAR NOT NULL,
    year VARCHAR,
    author_id INTEGER REFERENCES authors
);

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    rating integer NOT NULL,
    content VARCHAR NOT NULL,
    user_id INTEGER NOT NULL REFERENCES users,
    book_id INTEGER NOT NULL REFERENCES books
);