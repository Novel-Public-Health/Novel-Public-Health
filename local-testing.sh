# Comment what you don't need with '#'s

# Required. Installs required packages that the project uses. It's good practice to run this
# on each build, just in case a new package is added.
python -m pip install -r requirements.txt   ## Required ##

# Django will make migrations for any change to your models or fields.
python manage.py makemigrations             ## Required ##
python manage.py migrate                    ## Required ##

# This will copy all files from your static folders into the STATIC_ROOT directory.
python manage.py collectstatic --no-input   ## Required ##

# Runs the standard tests. These should all pass.
python manage.py test

# Creates a superuser for admin privileges.
python manage.py createsuperuser            ## Required only when you want to create an admin profile ##

# Syncs any subscription changes from stripe
python manage.py djstripe_sync_plans_from_stripe

# Runs a local server. Navigate to http://127.0.0.1:8000/ in any browser.
python manage.py runserver 127.0.0.1:8000   ## Required ##