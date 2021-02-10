# Novel Public Health
## Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/Novel-Public-Health/Novel-Public-Health.git
$ cd Novel-Public-Health

$ python3 -m venv gettingstarted # this might not work, shouldn't matter
$ pip install -r requirements.txt

$ createdb python_getting_started # skip this step for now

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local web -f Procfile.windows # for windows users
$ heroku local web # for mac users
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku
```
$ git add .
$ git commit -m "my commit"
$ git push origin main
```
or

***NOTE from Austin: the following is for deploying a heroku app manually from the CLI. We don't need to do this. Instead, we can test our changes on the local server, and the above git commands.***
```sh
$ heroku create
$ git push heroku main

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
