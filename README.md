# Project1 Books

# Heroku APP
To enter the application in Heroku, [here](https://bookcs-50.herokuapp.com/login).

# Books!
Hi! This is project1, it consists of a library of books. 📙

# Features
Search a book using:
 - ISBN 
 - Title
 - Author
 
Also, you can:
 - Login
 - Register

This library contains 5 thousand books, for each of them you can leave a review and a rating that goes from 1 to 5. For that the user must be registered. It is only allowed to leave one review per user for each book.

# Project structure 🗳️

This project contains the necessary configuration for its operation, in local mode and deployed in Heroku.

## Template 📂

Contains the html files that are rendered in the browser.

 - Layaout (Yep, 'Layaout')
 - Register
 - Login
 - Home
 - Search
 - Detail book
 - Nav
 - Error
 
Layaout, Nav and Error are used as templates.

## postgreSQL 📂

It contains the file with the queries with the structures of the tables used in the database and a couple of basic functions.

## Main directory 📂

Contains the main application and configuration files.

 - application.py 
	  > Main application
 - import.py
	 > Contains the function to export the books.csv file to the database
 - books.csv
	  >List of books, contains ISBN, Title, Author and Year of publication
 - requirements.txt
	 >Contains the modules necessary for the operation of the application in local and production (Heroku)
 - Procfile
	 >Procfile is used by Heroku in order to initialize the application correctly.

# Additional libraries or tools 🧰
This project is simple, so the additional libraries used are few:

 - Bootstrap: For the site interface. Make use of [this](https://getbootstrap.com/docs/4.0/examples/offcanvas/) template.
 - To get the covers of the books I use this [API](https://openlibrary.org/dev/docs/api/covers).
 - As source code editor: VSCode and AzureStudio for connection to the database.
 - To get the Emojis, [here](https://emojipedia.org/).
 - To design the README.md file easily, [here](https://stackedit.io/).
 - Heroku, to deploy the database and the application.

# Problems I had

 - When executing 'flask run' it showed an error like the following: *flask.cli.NoAppException*.
I solved it by uninstalling the Werkzeug module (Version 1) and reinstalling it but specifying the version: Werkzeug == 0.16.0.

 - When deploying the application in Heroku, I did not know that I had to include the Procfile file (it has no extension, just like that). Inside it goes the instruction so that the application can start correctly. It should be noted that within requirements.txt it is necessary to refer to 'Gunicorn' which is an HTTP server for Python.

