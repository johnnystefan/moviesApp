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
2.  Clone the repo and configure the virtual environment:

```
$ python -m virtualenv .env
$ cd .env
# Activate your virtualenv on Windows
$ \.env\Scripts\activate.bat
# Activate your virtualenv on Linux
$ source .env/Scripts/activate
$ pip install -r requirements.txt
$ git clone https://github.com/wsvincent/drfx.git
```

3.  Set up the initial migration for our custom user models in users and build the database.

```
(drfx) $ python manage.py makemigrations
(drfx) $ python manage.py migrate
(drfx) $ python manage.py createsuperuser
(drfx) $ python manage.py runserver
```

4.  Endpoints

Login with your superuser account. Then navigate to all users. Logout. Sign up for a new account and repeat the login, users, logout flow.

- login - http://127.0.0.1:8000/api/user/login
- logout - http://127.0.0.1:8000/logout/
- signup - http://127.0.0.1:8000/api/user/register

CRUD:

 - CREATE https://<your-domain>/api/movie/create
 - RETRIEVE a SINGLE https://<your-domain>/api/movie/<slug>/
 - RETRIEVE a LIST https://<your-domain>/api/movie/list
 - UPDATE https://<your-domain>/api/movie/<slug>/update
 - DELETE https://<your-domain>/api/movie/<slug>/delete
 - SEARCH http://<your-domain>/api/movie/list?search=johnny
 - ORDERING http://<your-domain>/api/movie/list?ordering=-date_updated
 - PAGINATION http://<your-domain>/api/movie/list?page=2
 - SEARCH + PAGINATION + ORDERING: <your-domain>/api/movie/list?search=johnny&page=2&ordering=-date_updated

---
