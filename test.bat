:: comment what you don't need

pip3 install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
 :: Run the standard tests. These should all pass.
::python manage.py test
:: Create a superuser, add 'heroku run' to the beginning of this statement to be a superuser for production too
::python manage.py createsuperuser
:: Sync any subscription changes from stripe
python .\manage.py djstripe_sync_plans_from_stripe
python manage.py runserver 127.0.0.1:8000