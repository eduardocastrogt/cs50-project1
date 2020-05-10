import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Db connection
engine = create_engine(os.getenv("DATABASE_URL").lstrip())
db = scoped_session(sessionmaker(bind=engine))

# Open
f = open("books.csv")
#Read
r = csv.reader(f)

for isbn, title, author, anio in r:
    db.execute("insert into Tbl_Book(ISBN, Title, Author, Year) values(:isbn, :title, :author, :year)", 
        {"isbn":isbn, "title":title, "author": author, "year": anio})
    db.commit()
    

