:: comment what you don't need

pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --no-input
 :: Run the standard tests. These should all pass.
python3 manage.py test
:: Create a superuser, add 'heroku run' to the beginning of this statement to be a superuser for production too
::python3 manage.py createsuperuser
python3 manage.py runserver 127.0.0.1:8000