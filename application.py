import os

from flask import Flask, session, render_template, request, redirect, url_for, flash, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker
from datetime import datetime
import requests


app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL").lstrip())
db = scoped_session(sessionmaker(bind=engine))


#Open connection
connection = db()


# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    
    if request.method == "POST":
        #Try get email
        exist_email = db.execute('select email from tbl_user where email = :email limit 1', 
            {"email":request.form.get("email")}).fetchone()

        if exist_email:
            return render_template("error.html", message = "the email exists.")

        if request.form.get("password") != request.form.get("cpassword"):
            return render_template("error.html", message = "the password should be the same.")

        db.execute('select public.Book_SaveUser(:name_, :lastname_, :email_, :password_)',
            {"name_": request.form.get("name"), "lastname_": request.form.get("lastname"), "email_" :request.form.get("email"), 
            "password_" : request.form.get("password")})
        db.commit()

        session["user"] = db.execute('select * from public.Book_ExistUser(:email, :password)',
        {"email": request.form.get("email"), "password": request.form.get("password")}).fetchone()

    return redirect("/home")

# Login route
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        session["user"] = db.execute('select * from public.Book_ExistUser(:email, :password)',
        {"email": request.form.get("email"), "password": request.form.get("password")}).fetchone()

    if session["user"] == None:
        return render_template("error.html", message = "email or password invalid.")

    return redirect(url_for("home"))

# Home page
@app.route("/home", methods=["GET", "POST"])
def home():

    if session.get("user") == None:
        return redirect("/login")

    if request.method == "GET":
        return render_template("home.html")

    if request.method == "POST":
        
        libros = db.execute("select *  from Tbl_Book where isbn ilike :search_ or title ilike :search_ or author ilike :search_ limit 20",
            {"search_": "%" + request.form.get("search")+"%" }).fetchall()

        if len(libros) == 0:
            return render_template("error.html", message="sorry, your search is empty")
        else:
            print("Si hay libros")
            return render_template("search.html", search=libros)

#Book detail
@app.route("/book/<isbn>", methods=["GET", "POST"])
def book(isbn):
    if session.get("user") is None:
        return redirect("/login")

    if request.method == "GET":
        #Book information
        session["book"] = db.execute("select * from tbl_book where isbn = :isbn_", 
            {"isbn_": isbn}).fetchone()
        session["review"] = db.execute('select comment, count_review, concat(name,' + "' " + "'" + ',lastname) as user, register from Tbl_Review a inner join Tbl_User b on a.Id_User = b.Id_User where a.isbn = :isbn_',
             {"isbn_": isbn}).fetchall()

        #Get the key
        key = os.getenv("GOODREADS_KEY")
        #Request from Goodreads
        goodreads = requests.get("https://www.goodreads.com/book/review_counts.json",
                params={"key": key, "isbns": isbn})

        #Parse json
        if goodreads is not None:
            response = goodreads.json()

        return render_template("detail_book.html", book = session["book"], bookinfo = response['books'][0], review = session["review"])

    if request.method == "POST":
        
        if request.form.get("comment") is None or request.form.get("comment") == "":
            flash("the comment is necessary")
            return redirect("/book/" + isbn)
        
        #Current date
        dt = datetime.now()

        #Save data
        try:
            db.execute("insert into Tbl_Review(id_user, isbn, comment, count_review, register) values(:iduser_, :isbn_, :comment_, :point_, :date_)",
                {"iduser_": session["user"][0], "isbn_": session["book"][1], 
                    "comment_": request.form.get("comment"), "point_": request.form.get("points"), "date_": dt})
            db.commit()

            flash("Your comment has be saved.")
        except:
            flash("Maybe you already wrote a comment")

    return redirect("/book/" + isbn)

@app.route("/logout")
def logout():
    session["user"] = None
    return redirect("/login")


@app.route("/api/<isbn>")
def api(isbn):

    book_api = db.execute('select a.title, a.author, a.year, a.isbn, count(b.Id_Review) as review_count, coalesce(avg(b.Count_review),0) as average_score from Tbl_book a left join Tbl_Review b on a.isbn = b.isbn where a.isbn = :isbn_ group by a.title, a.author, a.year, a.isbn',
        {"isbn_": isbn}).fetchone()

    if book_api is None:
        return jsonify({"Message": "ISBN does not exist."}), 404
        
    return jsonify(dict(book_api.items()))
