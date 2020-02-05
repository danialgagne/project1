import csv


with open('books.csv', 'r') as f:
    reader = csv.reader(f)

    #skip header row
    next(reader, None)
    authors = {row[2] for row in reader}
    for author in authors:
        db.execute("INSERT INTO authors (name) values (:name)", {"name": author})
