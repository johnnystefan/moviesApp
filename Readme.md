# OMNI

Omni is a Django Project with Django Rest Framework. Your RESTful API comes with a custom user model, login / logout / user registration / Change and password recovery. It also has a CRUD of Movies, in addition, Search and ordering of Movies.

## Features

- Django 2.2 and Python 3.8
- Custom user model
- Token-based auth
- RESTful API
- Signup/login/logout
- change and Retrieve password
- CRUD
- Search and Ordering.

## First-time setup

1.  Make sure Python 3.8x and Virtualenv are already installed.

```
$ git clone https://github.com/johnnystefan/moviesApp.git
$ cd moviesApp
$ python -m virtualenv .env
# Activate your virtualenv on Windows
$ \.env\Scripts\activate.bat
# Activate your virtualenv on Linux
$ source .env/Scripts/activate
$ pip install -r requirements.txt
$ mkdir temp
```

3.  Set up the initial migration for our custom user models in users and build the database.

```
(.env) $ python manage.py makemigrations movies
(.env) $ python manage.py makemigrations users
(.env) $ python manage.py migrate
(.env) $ python manage.py createsuperuser
(.env) $ python manage.py runserver
```

4.  Endpoints

Login with your superuser account. Then navigate to all users. Logout. Sign up for a new account and repeat the login, users, logout flow.

- login - http://127.0.0.1:8000/api/user/login
- logout - http://127.0.0.1:8000/logout/
- signup - http://127.0.0.1:8000/api/user/register

CRUD:

 - CREATE - http://127.0.0.1:8000/api/movie/create
 - RETRIEVE a SINGLE - http://127.0.0.1:8000/api/movie/<slug>/
 - RETRIEVE a LIST - http://127.0.0.1:8000/api/movie/list
 - UPDATE - http://127.0.0.1:8000/api/movie/<slug>/update
 - DELETE - http://127.0.0.1:8000/api/movie/<slug>/delete
 - SEARCH - http://127.0.0.1:8000/api/movie/list?search=johnny
 - ORDERING - http://127.0.0.1:8000/api/movie/list?ordering=-date_updated
 - PAGINATION - http://127.0.0.1:8000/api/movie/list?page=2
 - SEARCH + PAGINATION + ORDERING: - http://127.0.0.1:8000/api/movie/list?search=johnny&page=2&ordering=-date_updated

---
