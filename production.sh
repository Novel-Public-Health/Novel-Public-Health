# Django will make migrations for any change to your models or fields.
heroku run python manage.py makemigrations --app novel-public-health                    ## Required ##
heroku run python manage.py migrate --app novel-public-health                           ## Required ##
heroku run python manage.py collectstatic --no-input --app novel-public-health          ## Required ##
heroku run python manage.py djstripe_sync_plans_from_stripe --app novel-public-health   ## Required ##

# Creates a superuser for admin privileges on the production site (e.g. https://novel-public-health.herokuapp.com/admin/)
heroku run python manage.py createsuperuser --app novel-public-health                   ## Required only when you want to create an admin profile ##