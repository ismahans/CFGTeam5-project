    This work is part of the CodeFirstGirls Software Nanodegree
### Code First Girls Software NanoDegree Group Project
    *Group members: Ismahan Ali, Lucia Barrios, Maymuna Mohamed, Princess Ann Quilang, Suki Law*
![Logo](https://github.com/LuciaBV/CFGProject/blob/3fdc41172e61c9b43e91d8aa287bf67be998eb95/myapp/static/FitLifeWebsite/images/Screenshot%202022-10-25%20at%2020.23.52.png)

#### This repository contains the code needed to launch the gym class booking app.

### About

This project is a reusable booking system for new or existing gyms. FitLife creates a simple way to search for classes specific to the body parts the user wishes to target and allows users to book into classes without the need for binding gym memberships.

FitLife allows users to create user profiles, search and access class schedules and book onto classes. Once bookings are made, users can view existing booking and cancel.

The program is built using python, django, html and utilises sqlite databases. 

:open_book: Text files:

├----Project Report - *insert file name*

:open_file_folder: Programme files:

    ├── MyApp
        └── Migrations
        └── Static
            ├── images
        └── templates 
            ├── myapp
                └── base.html
                └── bookings.html
                └── booklist.html
                └── error.html
                └── findclass.html
                └── home.html
                └── list.html
                └── signin.html
                └── success.html
                └── thank.html
        └── __init__.py
        └── admin.py   
        └── apps.py
        └── forms.py
        └── models.py
        └── tests.py
        └── urls.py
        └── views.py
    ├── myproject
        └── __init__.py
        └── settings.py
        └── urls.py
        └── wsgi.py
    ├── venv
    ├── .gitignore
    ├── db.sqlite3
    ├── manage.py
    ├── README.md

### Getting started
1. Clone the git repository and pip install the following packages:

   - django

2. Run the following commands in the terminal:
    
   - python manage.py migrate
3. To run the server run the following command in the terminal:

   - python manage.py runserver

4. Click the generated server url to browse the app. 

   - http://127.0.0.1:8000/

### Creating Admin details and making class schedules
1. To create an admin login, run the command:

   - python manage.py createsuperuser 

   - follow the prompts for username and password creation
   
   - rerun python manage.py runserver

2. To access admin pages (used to populate class schedules) use the generated link and add 'admin'
    
- eg. http://127.0.0.1:8000/admin

Once you've entered your class details, your users can now use the user url to register and log in. Once logged in, users can now book onto your classes.
