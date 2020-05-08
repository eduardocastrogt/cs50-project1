import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import scoped_session, sessionmaker
import requests


app = Flask(__name__)

# Get database_url


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

@app.route("/")
def index():
    return "Project 1: TODO"

#Test route
@app.route("/template")
def template():
    return render_template("layaout.html", title="Holis")

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

    return "Gracias"

