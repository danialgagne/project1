import os
import csv
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


def import_authors():
    with open('books.csv', 'r') as f:
        reader = csv.reader(f)

        #skip header row
        next(reader, None)
        authors = {row[2] for row in reader}

        for author in authors:
            print(author)
            db.execute("INSERT INTO authors (name) VALUES (:name)", {"name": author})
        db.commit()

def import_books():
    with open('books.csv', 'r') as f:
        reader = csv.reader(f)

        #skip header row
        next(reader, None)
        for row in reader:
            author = db.execute("SELECT * FROM authors WHERE name = :name",
                                {"name": row[2]}).first()
            author_id = author.id
            print(f"{author.id}: {author.name}, book: {row[1]}")
            db.execute("""
                        INSERT INTO books (isbn, title, year, author_id)
                        VALUES (:isbn, :title, :year, :author_id)""",
                        {"isbn": row[0], "title": row[1],
                        "year": row[3], "author_id": author_id})
        db.commit()

if __name__ == "__main__":
    import_authors()
    import_books()
