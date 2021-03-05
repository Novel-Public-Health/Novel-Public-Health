#!/bin/bash
# comment what you don't need

# pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic # say yes
python3 manage.py test # Run the standard tests. These should all pass.
# Create a superuser, add 'heroku run' to the beginning of this statement to be a superuser for production too
# python3 manage.py createsuperuser
python3 manage.py runserver