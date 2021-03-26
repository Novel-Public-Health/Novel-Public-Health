# Novel Public Health
Tutorial "Local Library" website written in Django.

For detailed information about this project see the associated [MDN tutorial home page](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Tutorial_local_library_website).

## Overview

This web application creates an online catalog for a small local library, where users can browse available books and manage their accounts.

The main features that have currently been implemented are:

* There are models for books, book copies, genre, language and authors.
* Users can view list and detail information for books and authors.
* Admin users can create and manage models. The admin has been optimised (the basic registration is present in admin.py, but commented out).
* Librarians can renew reserved books

![Local Library Model](https://raw.githubusercontent.com/mdn/django-locallibrary-tutorial/master/catalog/static/images/local_library_model_uml.png)


## Quick Start

To get this project up and running locally on your computer:
1. Set up the [Python development environment](https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment).
   We recommend using a Python virtual environment.
1. Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or `py -3` instead of `python` to start Python):
   ```
   python -m pip install -r requirements.txt
   python manage.py makemigrations
   python manage.py migrate
   python manage.py collectstatic
   python manage.py test # Run the standard tests. These should all pass.
   # Create a superuser
   python manage.py createsuperuser
   python manage.py runserver 127.0.0.1:8000
   ```
1. Open a browser to `http://127.0.0.1:8000/admin/` to open the admin site
1. Create a few test objects of each type.
1. Open tab to `http://127.0.0.1:8000` to see the main site, with your new objects.

## Deploying to Heroku
```
> git add .
> git commit -m "my commit"
> git push origin main
```

Additional production commands after making migrations.
```
> heroku run python manage.py makemigrations --app novel-public-health
> heroku run python manage.py migrate --app novel-public-health
> heroku run python manage.py collectstatic --no-input --app novel-public-health

> heroku run python manage.py test --app novel-public-health
# Create a superuser, add 'heroku run' to the beginning of this statement to be a superuser for production too
> heroku run python manage.py createsuperuser --app novel-public-health
```

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
