import os
from dotenv import load_dotenv
import requests

from flask import abort, Flask, flash, jsonify, session, \
    redirect, render_template, request, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")
if not os.getenv("GOODREADS_API_KEY"):
    raise RuntimeError("GOODREADS_API_KEY is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if 'id' in session:
        search_term = request.args.get('search-input')

        if search_term is None:
            results = []
        else:
            search_term = search_term.lower()
            results = db.execute(
                f"SELECT books.isbn as isbn, books.title as title, books.year as year, authors.name as name FROM books JOIN authors ON authors.id = books.author_id WHERE (LOWER(title) LIKE '%{search_term}%' OR LOWER(isbn) LIKE '%{search_term}%' OR LOWER(name) LIKE '%{search_term}%');"
            ).fetchall()
            
        return render_template("index.html", results=results, count=len(results))
    return redirect(url_for('login'))


@app.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username-input')
        password = request.form.get('password-input')
        
        db.execute("INSERT INTO users (username, password) VALUES (:username, :password)",
                {"username": username, "password": password})
        db.commit()

        flash("Registered successfully!")
        return redirect(url_for('index'))
    else:
        return render_template("sign_up.html")
    # TODO: catch unique username constraint

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form.get('username-input')
        password = request.form.get('password-input')

        user = db.execute("""
                            SELECT * FROM users 
                            WHERE username = :username 
                            AND password = :password""",
                            {"username": username, "password": password})
        if user.rowcount == 1:
            session['id'] = user.first().id
            flash('signed in successfully')
            return redirect(url_for('index'))
        else:
            flash('invalid username/password')
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('id', None)
    return redirect(url_for('login'))

@app.route("/book/<isbn>", methods=["GET", "POST"])
def book(isbn):
    book_details = db.execute(
        """
        SELECT
            books.id AS book_id,
            books.author_id AS author_id,
            books.isbn AS isbn,
            books.title AS title,
            books.year AS year,
            authors.name AS name
        FROM books 
        JOIN authors 
        ON authors.id = books.author_id
        WHERE isbn = :isbn
        """,
        {"isbn": isbn}
    ).first()

    res = requests.get(
        "https://www.goodreads.com/book/review_counts.json",
        params={"key": os.getenv("GOODREADS_API_KEY"),
                "isbns": isbn}
    )
    goodreads_ratings = res.json()["books"][0]

    if 'id' in session:
        user_id = session['id']
        book_id = book_details.book_id

        user_book_reviews = db.execute(
            """
            SELECT * FROM reviews 
            WHERE user_id = :user_id AND book_id = :book_id""",
            {"user_id": user_id, "book_id": book_id}
        ).first()

        if user_book_reviews is not None:
            return render_template(
                "book.html",
                book_details=book_details,
                user_book_reviews=user_book_reviews,
                goodreads_ratings=goodreads_ratings
            )

        if request.method == "POST":
            rating = request.form.get('rating-select')
            content = request.form.get('review-text')

            db.execute(
                """
                INSERT INTO reviews (rating, content, user_id, book_id)
                VALUES (:rating, :content, :user_id, :book_id)""",
                {"rating": rating, "content": content,
                "user_id": user_id, "book_id": book_id}
            )
            db.commit()
            return redirect(url_for('book', isbn=isbn))

    return render_template(
        "book.html",
        book_details=book_details,
        goodreads_ratings=goodreads_ratings
    )

@app.route("/api/<isbn>")
def api(isbn):
    book_details = db.execute(
        """
        SELECT
            books.id AS book_id,
            books.author_id AS author_id,
            books.isbn AS isbn,
            books.title AS title,
            books.year AS year,
            authors.name AS name
        FROM books 
        JOIN authors 
        ON authors.id = books.author_id
        WHERE isbn = :isbn
        """,
        {"isbn": isbn}
    ).first()

    if book_details is None:
        abort(404)

    res = requests.get(
        "https://www.goodreads.com/book/review_counts.json",
        params={"key": os.getenv("GOODREADS_API_KEY"),
                "isbns": isbn}
    )
    goodreads_ratings = res.json()["books"][0]

    return jsonify({
        "title": book_details.title,
        "author": book_details.name,
        "year": book_details.year,
        "isbn": book_details.isbn,
        "review_count": goodreads_ratings["ratings_count"],
        "average_score": goodreads_ratings["average_rating"]
    })
