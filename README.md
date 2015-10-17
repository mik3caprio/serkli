# serkli
Create Circles Of Support To Prevent Breast Cancer

## To Get Running
This assumes you have already gone through all the install procedures for Homebrew, python, postgreSQL. If you need more info on those, please see the wiki.

* `source venv/bin/activate`
* `source venv/bin/postactivate`
* `pip install -r requirements.txt`
* `python manage.py makemigrations`
* `python manage.py migrate`
* `python manage.py runserver`

## Deploy to production

* `git push heroku master && heroku run --app circlyorg python manage.py migrate`
