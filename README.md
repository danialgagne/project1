# Project 1 - Book Review Site

Web Programming with Python and JavaScript

Project 1 asks students to create a site for users to search for books, view the book review statistics, and submit their own reviews. Users who log in are able to search and submit reviews (once per book), while non-logged in users can still find individual results by navigating to the `book/isbn` url, although they can't submit reviews. An api endpoint has also been set up so users can get basic book information and review statistics in json format.

## Getting Started

To clone and run this application, you'll need [Git](https://git-scm.com), [Pip](https://pip.pypa.io/en/stable/installing/), [PostgreSQL](https://www.postgresql.org/download/), and [Python](https://www.python.org/) version 3.7 (or higher) installed.

### PostgreSQL

For this project, you’ll need to set up a PostgreSQL database to use with the application. It’s possible to set up PostgreSQL locally on your own computer, or use a database hosted by Heroku, an online web hosting service.

1. Navigate to https://www.heroku.com/, and create an account if you don’t already have one.
2. On Heroku’s Dashboard, click “New” and choose “Create new app.”
3. Give your app a name, and click “Create app.”
4. On your app’s “Overview” page, click the “Configure Add-ons” button.
5. In the “Add-ons” section of the page, type in and select “Heroku Postgres.”
6. Choose the “Hobby Dev - Free” plan, which will give you access to a free PostgreSQL database that will support up to 10,000 rows of data. Click “Provision.”
7. Now, click the “Heroku Postgres :: Database” link.
8. You should now be on your database’s overview page. Click on “Settings”, and then “View Credentials.” This is the information you’ll need to log into your database. You can access the database via Adminer, filling in the server (the “Host” in the credentials list), your username (the “User”), your password, and the name of the database, all of which you can find on the Heroku credentials page.

Alternatively, if you install PostgreSQL on your own computer, you should be able to run psql URI on the command line, where the URI is the link provided in the Heroku credentials list.

### Goodreads API

Goodreads is a popular book review website, and we’ll be using their API in this project to get access to their review data for individual books.

1. Go to https://www.goodreads.com/api and sign up for a Goodreads account if you don’t already have one.
2. Navigate to https://www.goodreads.com/api/keys and apply for an API key. For “Application name” and “Company name” feel free to just write “project1,” and no need to include an application URL, callback URL, or support URL.
3. You should then see your API key. (For this project, we’ll care only about the “key”, not the “secret”.)
4. You can now use that API key to make requests to the Goodreads API, documented here. In particular, Python code like the below

## Installing

To start, clone the repository and set up your environment with the required dependencies from the `requirements.txt` file.


```bash
# Clone this repository
$ git clone https://github.com/danialgagne/project1.git

# Go into the repository
$ cd project1

# Install the dependencies
$ pip install -r requirements.txt
```

You'll need to copy and rename the `.env.sample` file to `.env` with the following environment variables set:

```
FLASK_APP=application.py
DATABASE_URL=your_database_uri
GOODREADS_API_KEY=your_api_key
```

Connect to your database using using Adminer or the `psql` command, and create your database tables by copy and pasting each `CREATE` command from the `create_tables.sql` file.

The app is now ready to run, although without books loaded into your database, the functionality is limited. The `import.py` script will load your database with 5,000 books and 1,910 authors.

```bash
# Load the database with book information
$ python import.py

# Run the app
$ flask run
```