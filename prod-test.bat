heroku run python manage.py makemigrations --app novel-public-health ^
& heroku run python manage.py migrate --app novel-public-health ^
& heroku run python manage.py collectstatic --no-input --app novel-public-health

 :: Run the standard tests. These should all pass.
::& heroku run python manage.py test --app novel-public-health
:: Create a superuser, add 'heroku run' to the beginning of this statement to be a superuser for production too
::& heroku run python manage.py createsuperuser --app novel-public-health