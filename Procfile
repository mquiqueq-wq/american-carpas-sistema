release: python manage.py migrate && python setup_superuser.py
web: gunicorn american_carpas_1.wsgi:application --bind 0.0.0.0:$PORT
