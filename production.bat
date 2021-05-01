heroku run python manage.py makemigrations --app novel-public-health ^
& heroku run python manage.py migrate --app novel-public-health ^
& heroku run python manage.py collectstatic --no-input --app novel-public-health ^
& heroku run python manage.py djstripe_sync_plans_from_stripe --app novel-public-health
::& heroku run python manage.py createsuperuser --app novel-public-health ^