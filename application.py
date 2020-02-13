import os
from dotenv import load_dotenv

from flask import Flask, flash, session, \
    redirect, render_template, request, url_for
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()
app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if 'username' in session:
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
            session['username'] = username
            flash('signed in successfully')
            return redirect(url_for('index'))
        else:
            flash('invalid username/password')
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))
